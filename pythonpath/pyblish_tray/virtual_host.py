from PyQt5 import QtCore

import pyblish_qml


class Controller(QtCore.QObject):
    """The primary controller for the virtual host"""

    def __init__(self, parent=None):
        super(Controller, self).__init__(parent)

        self.proxy = None
        self.port = None
        self.thread = None
        self.server = None

    @QtCore.pyqtSlot()
    def show(self):
        if self.proxy is None:
            print("Proxy not initialised")
            return

        settings = pyblish_qml.settings.to_dict()
        self.proxy.show(self.port, settings)

    def kill(self):
        self.server.shutdown()
