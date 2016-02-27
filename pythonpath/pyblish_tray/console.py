from PyQt5 import QtCore, QtWidgets


class Model(QtCore.QAbstractListModel):
    def __init__(self, items=None, parent=None):
        super(Model, self).__init__(parent)
        self._items = items or list()

    def data(self, index, role=QtCore.QModelIndex()):
        names = self.role_names()
        if role in names.keys():
            name = names[role]
            return self._items[index.row()].get(name)

    def set_data(self, value, row, role_name):
        item = self._items[row]
        index = self.createIndex(row, 0)
        item[role_name] = value

        self.dataChanged.emit(index, index)

    def clear_data(self, value, role_name):
        for row, item in enumerate(self._items):
            item[role_name] = value

        # Change all data
        self.dataChanged.emit(
            self.createIndex(0, 0),
            self.createIndex(len(self._items), 0)
        )

    def add_item(self, item):
        """Add new item to model"""

        self.beginInsertRows(QtCore.QModelIndex(),
                             self.row_count(),
                             self.row_count())

        self._items.append(item)
        self.endInsertRows()

    def row_count(self, parent=None):
        return len(self._items)

    def role_names(self):
        return {
            QtCore.Qt.UserRole + 0: "line",
            QtCore.Qt.UserRole + 1: "selected",
        }

    # Qt naming convention conversion
    roleNames = role_names
    rowCount = row_count


def prop(attr):
    """A constant PyQt property"""
    return QtCore.pyqtProperty(QtCore.QVariant,
                               fget=attr,
                               constant=True)


class Controller(QtCore.QObject):
    """The primary controller for the console"""

    model = prop(lambda self: self._model)

    autohideChanged = QtCore.pyqtSignal(bool)
    focusChanged = QtCore.pyqtSignal(bool)

    copied = QtCore.pyqtSignal()
    cleared = QtCore.pyqtSignal()
    allSelected = QtCore.pyqtSignal()

    selectionStarted = QtCore.pyqtSignal(int, int)  # startIndex, endIndex
    selectionChanged = QtCore.pyqtSignal(int, int)
    selectionEnded = QtCore.pyqtSignal(int, int)

    def __init__(self, parent=None):
        super(Controller, self).__init__(parent)

        self._model = Model()
        self.popen = None

        self.selectionChanged.connect(self.on_selection_changed)
        self.selectionStarted.connect(self.on_selection_started)
        self.selectionEnded.connect(self.on_selection_changed)

        QtWidgets.qApp.is_broadcasting.connect(
            self.on_application_broadcasting)

    @QtCore.pyqtSlot()
    def copy(self):
        """Copy currently selected text in the console"""
        clipboard = QtWidgets.qApp.clipboard()
        clipboard.setText("\n".join(
            i["line"] for i in self._model._items
            if i["selected"]
        ))
        self.copied.emit()

    @QtCore.pyqtSlot()
    def clear(self):
        """Clear currently selected text in the console"""
        self._model.clear_data(False, "selected")
        self.cleared.emit()

    @QtCore.pyqtSlot()
    def selectAll(self):
        """Select all text in the console"""
        self._model.clear_data(True, "selected")
        self.allSelected.emit()

    def on_application_broadcasting(self, text):
        """Respond to messages from QApplication"""
        self._model.add_item({
            "line": text,
            "selected": False
        })

    def on_selection_started(self, start, end):
        """Respond to changes in selection"""
        self._model.clear_data(False, "selected")

    def on_selection_changed(self, start, end):
        """Respond to changes in selection"""
        self._model.clear_data(False, "selected")

        for row in range(start, end + 1):
            self._model.set_data(True, row, "selected")
