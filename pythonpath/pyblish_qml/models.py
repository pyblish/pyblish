import time
import re
from PyQt5 import QtCore

import util
from pyblish_qml import settings


defaults = {
    "common": {
        "id": "default",
        "name": "default",
        "isProcessing": False,
        "families": list(),
        "familiesConcatenated": "",
        "isToggled": True,
        "hasError": False,
        "actionHasError": False,
        "actionPending": True,
        "succeeded": False,
        "processed": False,
        "currentProgress": 0,
        "duration": 0,          # Time (ms) to process pair
        "finishedAt": 0,        # Time (s) when finished
        "amountPassed": 0,      # Number of plug-ins/instances passed
        "amountFailed": 0,      # Number of plug-ins/instances failed
    },
    "plugin": {
        "doc": "",
        "order": None,
        "hasRepair": False,
        "optional": True,
        "hasCompatible": True,
        "hosts": list(),
        "type": "unknown",
        "module": "unknown",
        "compatibleInstances": list(),
        "contextEnabled": False,
        "instanceEnabled": False,
        "pre11": True,
        "verb": "unknown",
        "actions": list(),
        "actionsIconVisible": False,
        "path": "",
        "__instanceEnabled__": False
    },
    "instance": {
        "optional": True,
        "family": None,
        "niceName": "default",
        "compatiblePlugins": list(),
    },
    "result": {
        "type": "default",
        "filter": "default",
        "message": "default",

        # Temporary metadata: "default", until treemodel
        "instance": "default",
        "plugin": "default",

        # LogRecord
        "threadName": "default",
        "name": "default",
        "filename": "default",
        "pathname": "default",
        "lineno": 0,
        "msg": "default",
        "msecs": 0.0,

        # Exception
        "fname": "default",
        "line_number": 0,
        "func": "default",
        "exc": "default",

        # Context
        "port": 0,
        "host": "default",
        "user": "default",
        "connectTime": "default",
        "pythonVersion": "default",
        "pyblishVersion": "default",
        "endpointVersion": "default",

        # Plugin
        "doc": "default",
        "path": "default",
    }
}


class PropertyType(QtCore.pyqtWrapperType):
    """Metaclass for converting class attributes into pyqtProperties

    Usage:
        >>> class AbstractClass(QtCore.QObject):
        ...     __metaclass__ = PropertyType

    """

    prefix = "__pyqtproperty__"

    def __new__(cls, name, bases, attrs):
        """Convert class properties into pyqtProperties

        For use in conjuction with the :func:Item factory function.

        """

        for key, value in attrs.copy().items():
            if key.startswith("__"):
                continue

            notify = QtCore.pyqtSignal()

            def set_data(key, value):
                def set_data(self, value):
                    setattr(self, cls.prefix + key, value)
                    getattr(self, key + "Changed").emit()
                    self.__datachanged__.emit(self)
                return set_data

            attrs[key + "Changed"] = notify
            attrs[key] = QtCore.pyqtProperty(
                type(value) if value is not None else QtCore.QVariant,
                fget=lambda self, k=key: getattr(self, cls.prefix + k, None),
                fset=set_data(key, value),
                notify=notify)

        return super(PropertyType, cls).__new__(cls, name, bases, attrs)


class AbstractItem(QtCore.QObject):
    """Model Item

    See here for full details:
    https://github.com/pyblish/pyblish-qml/issues/81

    """

    __metaclass__ = PropertyType
    __datachanged__ = QtCore.pyqtSignal(QtCore.QObject)

    def __str__(self):
        return self.name

    def __repr__(self):
        return u"%s.%s(%r)" % (__name__, type(self).__name__, self.__str__())


def Item(**kwargs):
    """Factory function for QAbstractListModel items

    Any class attributes are converted into pyqtProperties
    and must be declared with its type as value.

    Special keyword "parent" is not passed as object properties
    but instead passed to the QObject constructor.

    Usage:
        >>> item = Item(name="default name",
        ...             age=5,
        ...             alive=True)
        >>> assert item.name == "default name"
        >>> assert item.age == 5
        >>> assert item.alive == True
        >>>
        >>> # Jsonifyable content
        >>> assert item.json == {
        ...     "name": "default name",
        ...     "age": 5,
        ...     "alive": True
        ...     }, item.json

    """

    parent = kwargs.pop("parent", None)
    cls = type("Item", (AbstractItem,), kwargs.copy())

    self = cls(parent)
    self.json = kwargs  # Store as json

    for key, value in kwargs.items():
        if hasattr(self, key):
            key = PropertyType.prefix + key
        setattr(self, key, value)

    return self


class AbstractModel(QtCore.QAbstractListModel):
    def __init__(self, parent=None):
        super(AbstractModel, self).__init__(parent)
        self.items = util.ItemList(key="id")

    @QtCore.pyqtSlot(int, result=QtCore.QObject)
    def item(self, index):
        return self.items[index]

    def add_item(self, item):
        """Add new item to model

        Each keyword argument is passed to the :func:Item
        factory function.

        """

        self.beginInsertRows(QtCore.QModelIndex(),
                             self.rowCount(),
                             self.rowCount())

        item["parent"] = self
        item = Item(**item)
        self.items.append(item)
        self.endInsertRows()

        item.__datachanged__.connect(self._dataChanged)

        return item

    def _dataChanged(self, item):
        """Explicitly emit dataChanged upon item changing"""
        index = self.items.index(item)
        qindex = self.createIndex(index, 0)
        self.dataChanged.emit(qindex, qindex)

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.items)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role in (QtCore.Qt.UserRole + 0, QtCore.Qt.UserRole + 1):
            try:
                return self.items[index.row()]
            except:
                pass

        return QtCore.QVariant()

    def roleNames(self):
        return {
            QtCore.Qt.UserRole + 0: "item",
            QtCore.Qt.UserRole + 1: "object"
        }

    def reset(self):
        self.beginResetModel()
        self.items[:] = []
        self.endResetModel()


def ItemIterator(items):
    for i in items:
        if i.name == "Context":
            continue

        if not i.isToggled:
            continue

        if not i.hasCompatible:
            continue

        yield i


class ItemModel(AbstractModel):
    def __init__(self, *args, **kwargs):
        super(ItemModel, self).__init__(*args, **kwargs)
        self.plugins = util.ItemList(key="id")
        self.instances = util.ItemList(key="id")

    def reorder(self, context):
        # Reorder instances in support of "cooperative collection"
        self.beginResetModel()

        items = dict()
        for instance in self.instances:
            items[instance.id] = instance
            self.items.remove(instance)

        # TODO: Clean this up. Instances are cached for
        # brevity but this is where we are forced to fight it.
        self.instances[:] = []
        self.items.append(items[context.id])
        self.instances.append(items[context.id])

        for instance in context:
            self.items.append(items[instance.id])
            self.instances.append(items[instance.id])

        self.endResetModel()

    @QtCore.pyqtSlot(QtCore.QVariant)
    def add_plugin(self, plugin):
        """Append `plugin` to model

        Arguments:
            plugin (dict): Serialised plug-in from pyblish-rpc

        Schema:
            plugin.json

        """

        item = {}
        item.update(defaults["common"])
        item.update(defaults["plugin"])

        for member in ["pre11",
                       "name",
                       "label",
                       "optional",
                       "category",
                       "actions",
                       "id",
                       "order",
                       "doc",
                       "type",
                       "module",
                       "hasRepair",
                       "families",
                       "contextEnabled",
                       "instanceEnabled",
                       "__instanceEnabled__",
                       "path"]:
            item[member] = plugin[member]

        # Visualised in Perspective
        item["familiesConcatenated"] = ", ".join(plugin["families"])

        # converting links to HTML
        pattern = r"(https?:\/\/(?:w{1,3}.)?[^\s]*?(?:\.[a-z]+)+)"
        pattern += r"(?![^<]*?(?:<\/\w+>|\/?>))"
        if item["doc"] and re.search(pattern, item["doc"]):
            html = r"<a href='\1'><font color='FF00CC'>\1</font></a>"
            item["doc"] = re.sub(pattern, html, item["doc"])

        # Append GUI-only data
        item["itemType"] = "plugin"
        item["hasCompatible"] = True
        item["isToggled"] = plugin.get("active", True)
        item["verb"] = {
            "Selector": "Collect",
            "Collector": "Collect",
            "Validator": "Validate",
            "Extractor": "Extract",
            "Integrator": "Integrate",
            "Conformer": "Integrate",
        }.get(item["type"], "Other")

        for action in item["actions"]:
            if action["on"] == "all":
                item["actionsIconVisible"] = True

        item = self.add_item(item)
        self.plugins.append(item)

    @QtCore.pyqtSlot(QtCore.QVariant)
    def add_instance(self, instance):
        """Append `instance` to model

        Arguments:
            instance (dict): Serialised instance

        Schema:
            instance.json

        """

        assert isinstance(instance, dict)

        item = defaults["common"].copy()
        item.update(defaults["instance"])

        item.update(instance["data"])
        item.update(instance)

        item["itemType"] = "instance"
        item["isToggled"] = instance["data"].get("publish", True)
        item["hasCompatible"] = True

        # Visualised in Perspective
        item["familiesConcatenated"] = instance["data"].get("family", "")
        item["familiesConcatenated"] += ", ".join(
            instance["data"].get("families", []))

        item = self.add_item(item)
        self.instances.append(item)

    @QtCore.pyqtSlot(QtCore.QVariant)
    def add_context(self, context, label=None):
        """Append `context` to model

        Arguments:
            context (dict): Serialised to add

        Schema:
            context.json

        """

        assert isinstance(context, dict)

        item = defaults["common"].copy()
        item.update(defaults["instance"])
        item.update(context)

        item["family"] = None
        item["label"] = context["data"].get("label") or settings.ContextLabel
        item["itemType"] = "instance"
        item["isToggled"] = True
        item["optional"] = False
        item["hasCompatible"] = True

        item = self.add_item(item)
        self.instances.append(item)

    def update_with_result(self, result):
        """Update item-model with result from host

        State is sent from host after processing had taken place
        and represents the events that took place; including
        log messages and completion status.

        Arguments:
            result (dict): Dictionary following the Result schema

        """

        for type in ("instance", "plugin"):
            id = (result[type] or {}).get("id")

            is_context = not id
            if is_context:
                item = self.instances[0]
            else:
                item = self.items.get(id)

            if item is None:
                # If an item isn't there yet
                # no worries. It's probably because
                # reset is still running and the
                # item in question is a new instance
                # not yet added to the model.
                continue

            item.isProcessing = False
            item.currentProgress = 1
            item.processed = True

            if result.get("error"):
                item.hasError = True
                item.amountFailed += 1

            else:
                item.succeeded = True
                item.amountPassed += 1

            item.duration += result["duration"]
            item.finishedAt = time.time()

            if item.itemType == "plugin":
                if item.actionsIconVisible:
                    continue

                actions = list(item.actions)

                # Context specific actions
                for action in list(actions):
                    if action["on"] == "failed" and not item.hasError:
                        actions.remove(action)
                    if action["on"] == "succeeded" and not item.succeeded:
                        actions.remove(action)
                    if action["on"] == "processed" and not item.processed:
                        actions.remove(action)

                if actions:
                    item.actionsIconVisible = True

    def has_failed_validator(self):
        for validator in self.plugins:
            if validator.order != 1:
                continue
            if validator.hasError:
                return True
        return False

    def reset_status(self):
        """Reset progress bars"""
        for item in self.items:
            item.isProcessing = False
            item.currentProgress = 0

    def update_compatibility(self):
        for plugin in self.plugins:
            has_compatible = False

            # A special clause for plug-ins only compatible
            # with the Context itself.
            if "Context" in plugin.compatibleInstances:
                has_compatible = True

            else:
                for instance in self.instances:
                    if not instance.isToggled:
                        continue

                    if instance.id in plugin.compatibleInstances:
                        has_compatible = True
                        break

            plugin.hasCompatible = has_compatible

    def reset(self):
        self.instances[:] = []
        self.plugins[:] = []
        super(ItemModel, self).reset()


class ResultModel(AbstractModel):

    added = QtCore.pyqtSignal()

    def add_item(self, item):
        item_ = defaults["result"].copy()
        item_.update(item)

        try:
            return super(ResultModel, self).add_item(item_)
        finally:
            self.added.emit()

    def add_context(self, context):
        item = defaults["result"].copy()
        item.update(context["data"])
        item.update({
            "type": "context",
            "name": "Pyblish",
            "filter": "Pyblish",
        })
        self.add_item(item)

    def update_with_result(self, result):
        parsed = self.parse_result(result)

        error = parsed.get("error")
        plugin = parsed.get("plugin")
        instance = parsed.get("instance")
        records = parsed.get("records")

        if getattr(self, "_last_plugin", None) != plugin["plugin"]:
            self._last_plugin = plugin["plugin"]
            self.add_item(plugin)

        self.add_item(instance)

        for record in records:
            self.add_item(record)

        if error is not None:
            self.add_item(error)

    def parse_result(self, result):
        plugin_name = result["plugin"]["name"]

        try:
            instance_name = result["instance"]["name"]
        except:
            instance_name = None

        plugin_msg = {
            "type": "plugin",
            "message": plugin_name,
            "filter": plugin_name,

            "plugin": plugin_name,
            "instance": instance_name
        }

        instance_msg = {
            "type": "instance",
            "message": instance_name or "Context",
            "filter": instance_name,
            "duration": result["duration"],

            "plugin": plugin_name,
            "instance": instance_name
        }

        record_msgs = list()

        for record in result["records"]:
            record["type"] = "record"
            record["filter"] = record["message"]
            record["message"] = util.format_text(str(record["message"]))

            record["plugin"] = plugin_name
            record["instance"] = instance_name

            record_msgs.append(record)

        error_msg = {
            "type": "error",
            "message": "No error",
            "filter": "",

            "plugin": plugin_name,
            "instance": instance_name
        }

        error_msg = None

        if result["error"] is not None:
            error = result["error"]
            error["type"] = "error"
            error["message"] = util.format_text(error["message"])
            error["filter"] = error["message"]

            error["plugin"] = plugin_name
            error["instance"] = instance_name

            error_msg = error

        return {
            "plugin": plugin_msg,
            "instance": instance_msg,
            "records": record_msgs,
            "error": error_msg,
        }


class ProxyModel(QtCore.QSortFilterProxyModel):
    """A QSortFilterProxyModel with custom exclude and include rules

    Role may be either an integer or string, and each
    role may include multiple values.

    Example:
        >>> # Exclude any item whose role 123 equals "Abc"
        >>> model = ProxyModel(None)
        >>> model.add_exclusion(role=123, value="Abc")

        >>> # Exclude multiple values
        >>> model.add_exclusion(role="name", value="Pontus")
        >>> model.add_exclusion(role="name", value="Richard")

        >>> # Exclude amongst includes
        >>> model.add_inclusion(role="type", value="PluginItem")
        >>> model.add_exclusion(role="name", value="Richard")

    """

    def __init__(self, source, parent=None):
        super(ProxyModel, self).__init__(parent)
        self.setSourceModel(source)

        self.excludes = dict()
        self.includes = dict()

    @QtCore.pyqtSlot(int, result=QtCore.QObject)
    def item(self, index):
        index = self.index(index, 0, QtCore.QModelIndex())
        index = self.mapToSource(index)
        model = self.sourceModel()
        return model.items[index.row()]

    @QtCore.pyqtSlot(str, str)
    def add_exclusion(self, role, value):
        """Exclude item if `role` equals `value`

        Attributes:
            role (int, string): Qt role or name to compare `value` to
            value (object): Value to exclude

        """

        self._add_rule(self.excludes, role, value)

    @QtCore.pyqtSlot(str, str)
    def remove_exclusion(self, role, value=None):
        """Remove exclusion rule

        Arguments:
            role (int, string): Qt role or name to remove
            value (object, optional): Value to remove. If none
                is supplied, the entire role will be removed.

        """

        self._remove_rule(self.excludes, role, value)

    def set_exclusion(self, rules):
        """Set excludes

        Replaces existing excludes with those in `rules`

        Arguments:
            rules (list): Tuples of (role, value)

        """

        self._set_rules(self.excludes, rules)

    @QtCore.pyqtSlot()
    def clear_exclusion(self):
        self._clear_group(self.excludes)

    @QtCore.pyqtSlot(str, str)
    def add_inclusion(self, role, value):
        """Include item if `role` equals `value`

        Attributes:
            role (int): Qt role to compare `value` to
            value (object): Value to exclude

        """

        self._add_rule(self.includes, role, value)

    @QtCore.pyqtSlot(str, str)
    def remove_inclusion(self, role, value=None):
        """Remove exclusion rule"""
        self._remove_rule(self.includes, role, value)

    def set_inclusion(self, rules):
        self._set_rules(self.includes, rules)

    @QtCore.pyqtSlot()
    def clear_inclusion(self):
        self._clear_group(self.includes)

    def _add_rule(self, group, role, value):
        """Implementation detail"""
        if role not in group:
            group[role] = list()

        group[role].append(value)

        self.invalidate()

    def _remove_rule(self, group, role, value=None):
        """Implementation detail"""
        if role not in group:
            return

        if value is None:
            group.pop(role, None)
        else:
            group[role].remove(value)

        self.invalidate()

    def _set_rules(self, group, rules):
        """Implementation detail"""
        group.clear()

        for rule in rules:
            self._add_rule(group, *rule)

        self.invalidate()

    def _clear_group(self, group):
        group.clear()

        self.invalidate()

    # Overridden methods

    def filterAcceptsRow(self, source_row, source_parent):
        """Exclude items in `self.excludes`"""
        model = self.sourceModel()
        item = model.items[source_row]

        key = getattr(item, "filter", None)
        if key is not None:
            regex = self.filterRegExp()
            if regex.pattern():
                match = regex.indexIn(key)
                return False if match == -1 else True

        for role, values in self.includes.items():
            data = getattr(item, role, None)
            if data not in values:
                return False

        for role, values in self.excludes.items():
            data = getattr(item, role, None)
            if data in values:
                return False

        return super(ProxyModel, self).filterAcceptsRow(
            source_row, source_parent)

    @QtCore.pyqtSlot(result=int)
    def rowCount(self, parent=QtCore.QModelIndex()):
        return super(ProxyModel, self).rowCount(parent)
