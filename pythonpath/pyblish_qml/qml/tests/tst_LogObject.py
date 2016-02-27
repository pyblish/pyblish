import sys
import logging

from PyQt5 import QtCore, QtGui, QtQuick


class Model(QtCore.QAbstractListModel):
    def __init__(self, parent=None):
        super(Model, self).__init__(parent)
        self.items = []

        # Keys available to us via LogRecord objects,
        # added via `addItem` below.
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
    """Custom handler to intercept log records that feed our `model`"""
    def __init__(self, model, *args, **kwargs):
        super(MessageHandler, self).__init__(*args, **kwargs)
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

engine = view.engine()
context = engine.rootContext()
context.setContextProperty("qmodel", proxy)

view.setSource(QtCore.QUrl("tst_LogObject.qml"))
view.setResizeMode(view.SizeRootObjectToView)
view.show()

handler = MessageHandler(model)

log = logging.getLogger()
log.addHandler(handler)
log.setLevel(logging.DEBUG)

log.info("Some information here")
log.info("Some more information")
log.warning("Don't go into the light!")
log.critical("You, sir, are done for.")
log.error("Does not compute")

app.exec_()
