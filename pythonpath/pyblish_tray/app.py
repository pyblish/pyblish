from __future__ import absolute_import

# Standard library
import os
import sys
import json
import threading
import subprocess

# Dependencies
import pyblish_rpc.server
import pyblish_qml.client
from PyQt5 import QtCore, QtWidgets, QtGui, QtQml

# Local
from . import console
from . import virtual_host


class Application(QtWidgets.QApplication):
    ROOTPATH = os.path.dirname(__file__)
    QMLPATH = os.path.join(ROOTPATH, "qml")
    MAINPATH = os.path.join(QMLPATH, "main.qml")
    ICONPATH = os.path.join(QMLPATH, "img/tray.png")
    THEMEPATH = os.path.join(ROOTPATH, "theme.json")

    is_broadcasting = QtCore.pyqtSignal(str)
    listening = QtCore.pyqtSignal()

    def __init__(self, argv):
        super(Application, self).__init__(argv)

        self._console_ctrl = console.Controller()
        self._tray = None
        self._popen = None
        self._window = None

        # Virtual host properties
        self._vhost_ctrl = virtual_host.Controller()

        with open(self.THEMEPATH) as f:
            self._theme = json.load(f)

        self.engine = QtQml.QQmlApplicationEngine()
        self.engine.addImportPath(self.QMLPATH)
        self.engine.objectCreated.connect(self.on_object_created)

        self.focusWindowChanged.connect(self.on_focus_changed)
        self._console_ctrl.autohideChanged.connect(
            self.on_autohide_changed)

        context = self.engine.rootContext()
        context.setContextProperty("applicationTheme", self._theme)
        context.setContextProperty("consoleCtrl", self._console_ctrl)
        context.setContextProperty("hostCtrl", self._vhost_ctrl)

        # Toggles
        self.toggles = {"autoHide": True}

        # Timers
        keep_visible = QtCore.QTimer(self)
        keep_visible.setInterval(1000)
        keep_visible.setSingleShot(True)

        self.timers = {"keepVisible": keep_visible}

    def start(self):
        self.engine.load(QtCore.QUrl.fromLocalFile(self.MAINPATH))
        self.exec_()

    def show(self):
        """Show the primary GUI

        This also activates the window and deals with platform-differences.

        """

        self._window.show()
        self._window.requestActivate()

        # Work-around for window appearing behind
        # other windows upon being shown once hidden.
        if os.name == "nt":
            old_flags = self._window.flags()
            new_flags = old_flags & QtCore.Qt.WindowStaysOnTopHint
            self._window.setFlags(new_flags)
            self._window.setFlags(old_flags)

        self.timers["keepVisible"].start()

    def broadcast(self, message):
        """Convenience method for emitting messages to the Controller"""
        print(message)
        self.is_broadcasting.emit(message)

    def on_tray_activated(self, reason):
        if self._window.isVisible():
            self._window.hide()

        elif reason == QtWidgets.QSystemTrayIcon.Trigger:
            self.show()

    def on_focus_changed(self, window):
        """Respond to window losing focus"""
        keep_visible = self.timers["keepVisible"].isActive()
        self._window.hide() if (self.toggles["autoHide"] and
                                not window and
                                not keep_visible) else None

    def on_object_created(self, obj, url):
        if not obj:
            return self.quit()

        self._window = obj

        self._tray = QtWidgets.QSystemTrayIcon(QtGui.QIcon(self.ICONPATH))
        self._tray.setToolTip("Pyblish")

        # Signals
        self._tray.activated.connect(self.on_tray_activated)
        self.aboutToQuit.connect(self.on_quit)
        self.listening.connect(self.launch_virtual_host)

        menu = self.build_menu()
        self._tray.setContextMenu(menu)
        self._tray.show()

        geometry = self.calculate_window_geometry()
        self._window.setGeometry(geometry)

        self.launch()

        self._tray.showMessage("Status",
                               "Pyblish is running. "
                               "Click here for more information.")

        if os.environ.get("DEBUG"):
            self._window.show()

    def on_autohide_changed(self, auto_hide):
        """Respond to changes to auto-hide

        Auto-hide is changed in the UI and determines whether or not
        the UI hides upon losing focus.

        """

        self.toggles["autoHide"] = auto_hide
        self.broadcast("Hiding when losing focus" if auto_hide
                       else "Stays visible")

    def on_quit(self):
        """Respond to the application quitting"""
        self.broadcast("Cleaning up..")
        self.broadcast("Hiding tray..")
        self._tray.hide()

        self.broadcast("Killing virtual host..")
        self._vhost_ctrl.kill()

        self.broadcast("Killing QML")
        self._popen.kill()

        self.broadcast("Shutting down..")

    def launch(self):
        """Launch external Pyblish QML and monitor process"""
        if self._popen:
            self._popen.kill()

        self.broadcast("Launching Pyblish QML..")

        popen = subprocess.Popen([sys.executable,
                                  "-u",  # Unbuffered stdout
                                  "-m", "pyblish_qml"],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT)

        def reader():
            for line in iter(popen.stdout.readline, b""):
                line = line.rstrip("\r\n")

                # TODO(marcus): Make this more robust
                if line.startswith("Listening on 127.0.0.1"):
                    self.listening.emit()

                self.broadcast(line)

        threading.Thread(target=reader).start()
        self.broadcast("Finished")
        self.broadcast("Listening for output..")

        # Store reference for cleanup
        self._popen = popen

    def launch_virtual_host(self):
        self.broadcast("Launching virtual host..")

        proxy = pyblish_qml.client.proxy()
        port = proxy.find_available_port()
        service = pyblish_rpc.service.RpcService()
        server = pyblish_rpc.server._server(port, service)
        os.environ["PYBLISH_CLIENT_PORT"] = str(port)

        thread = threading.Thread(target=server.serve_forever)
        thread.daemon = True  # Kill once parent dies
        thread.start()

        self.broadcast("Virtual server listening on"
                       "%s:%s" % server.server_address)

        self._vhost_ctrl.proxy = proxy
        self._vhost_ctrl.port = port
        self._vhost_ctrl.thread = thread
        self._vhost_ctrl.server = server

    def build_menu(self):
        menu = QtWidgets.QMenu()

        actions = (
            ("Open", self.show),
            ("Quit", self.quit)
        )

        for label, callback in actions:
            action = QtWidgets.QAction(label, self)
            action.triggered.connect(callback)
            menu.addAction(action)

        return menu

    def calculate_window_geometry(self):
        """Respond to status changes

        On creation, align window with where the tray icon is
        located. For example, if the tray icon is in the upper
        right corner of the screen, then this is where the
        window is supposed to appear.

        Arguments:
            status (int): Provided by Qt, the status flag of
                loading the input file.

        """

        tray_x = self._tray.geometry().x()
        tray_y = self._tray.geometry().y()

        width, height = self._window.width(), self._window.height()
        desktop_geometry = QtWidgets.QDesktopWidget().availableGeometry()
        screen_geometry = self._window.screen().geometry()

        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # Calculate width and height of system tray
        systray_width = screen_geometry.width() - desktop_geometry.width()
        systray_height = screen_geometry.height() - desktop_geometry.height()

        padding = 10

        x = screen_width - width
        y = screen_height - height

        if tray_x < (screen_width / 2):
            x = 0 + systray_width + padding
        else:
            x -= systray_width + padding

        if tray_y < (screen_height / 2):
            y = 0 + systray_height + padding
        else:
            y -= systray_height + padding

        return QtCore.QRect(x, y, width, height)


def main(debug=False):
    app = Application(sys.argv)

    if debug:
        os.environ["DEBUG"] = "1"
        __import__("_debug").bootstrap(app)

    app.start()


if __name__ == "__main__":
    # main(debug=True)
    main()
