import sys
import logging

from PyQt5 import QtCore, QtGui, QtQuick


class Model(QtCore.QAbstractListModel):
    def __init__(self, parent=None):
        super(Model, self).__init__(parent)
        self.items = []
        self.roles = {
            257: "threadName",
            258: "name",
            259: "thread",
            260: "created",
            261: "process",
            262: "processName",
            263: "args",
            264: "module",
            265: "filename",
            266: "levelno",
            267: "exc_text",
            268: "pathname",
            269: "lineno",
            270: "msg",
            271: "exc_info",
            272: "funcName",
            273: "relativeCreated",
            274: "levelname",
            275: "msecs",
        }

    def addItem(self, item):
        self.beginInsertRows(QtCore.QModelIndex(),
                             self.rowCount(),
                             self.rowCount())

        self.items.append(item.__dict__)
        self.endInsertRows()

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.items)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        try:
            item = self.items[index.row()]
        except IndexError:
            return QtCore.QVariant()

        if role in self.roles:
            return item.get(self.roles[role], QtCore.QVariant())

        return QtCore.QVariant()

    def roleNames(self):
        return self.roles


class MessageHandler(logging.Handler):
    def __init__(self, model, *args, **kwargs):
        logging.Handler.__init__(self, *args, **kwargs)
        self.model = model

    def emit(self, record):
        self.model.addItem(record)


app = QtGui.QGuiApplication(sys.argv)

view = QtQuick.QQuickView()

model = Model()
proxy = QtCore.QSortFilterProxyModel()
proxy.setSourceModel(model)
proxy.setFilterRole(model.roles.keys()[0])
proxy.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)


class Control(QtCore.QObject):
    """Controller

    This object is only used to synchronise a list
    between Python and QML; it's messy and not ideal.

    """

    _levels = "INFO;WARNING"

    @QtCore.pyqtProperty(str)
    def levels(self):
        return self._levels

    @QtCore.pyqtSlot(str)
    def updateLevels(self, levels):
        self._levels = levels
        proxy.invalidate()

control = Control()


def filterAcceptsRow(source_row, source_parent):
    """Exclude levels

    Overridden in order to exclude any log-record
    that isn't part of Control._levels

    """

    row = model.items[source_row]

    if not row["levelname"] in control._levels.split(";"):
        return False

    return QtCore.QSortFilterProxyModel.filterAcceptsRow(
        proxy, source_row, source_parent)

proxy.filterAcceptsRow = filterAcceptsRow

engine = view.engine()
context = engine.rootContext()
context.setContextProperty("qmodel", proxy)
context.setContextProperty("control", control)

view.setSource(QtCore.QUrl("tst_LogObjectMulti.qml"))
view.setResizeMode(view.SizeRootObjectToView)
view.show()

handler = MessageHandler(model)

log = logging.getLogger()
log.addHandler(handler)
log.setLevel(logging.DEBUG)

# Test data
log.debug("e = mc^2")
log.info("Some information here")
log.info("Some more information")
log.warning("Don't go into the light!")
log.critical("You, sir, are done for.")
log.error("Does not compute")

app.exec_()
