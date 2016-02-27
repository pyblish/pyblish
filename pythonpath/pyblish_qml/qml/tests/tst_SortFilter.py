import sys
from PyQt5 import QtCore, QtGui, QtQuick


class Model(QtCore.QAbstractListModel):
    def __init__(self, parent=None):
        super(Model, self).__init__(parent)
        self.items = [
            {"name": "Item1"},
            {"name": "Item2"},
            {"name": "Item3"},
            {"name": "Item4"},
            {"name": "Item5"},
            {"name": "Item6"},
            {"name": "Item12"},
            {"name": "Item13"},
            {"name": "Item14"},
        ]
        self.roles = {
            QtCore.Qt.UserRole + 1: "name"
        }

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

view.setSource(QtCore.QUrl("tst_SortFilter.qml"))
view.setResizeMode(view.SizeRootObjectToView)
view.show()

app.exec_()
