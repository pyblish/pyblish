"""Pyblish QML RPC server

Attributes:
    first_port (int): Port at which to start distributing
        available ports to clients who ask for one.

"""

import os

try:
    from SimpleXMLRPCServer import SimpleXMLRPCServer
except ImportError:
    # Python 3
    from xmlrpc.server import SimpleXMLRPCServer

first_port = 9001


class QmlApi(object):
    def __init__(self, app):
        self.app = app
        self.ctrl = CtrlApi(app.controller)

    def show(self, port, settings=None):
        """Show the GUI

        Arguments:
            port (int): Port with which to communicate with client
            settings (optional, dict): Client settings

        """

        self.app.show_signal.emit(port, settings)
        return True

    def hide(self):
        """Hide the GUI"""
        self.app.hide_signal.emit()
        return True

    def quit(self):
        """Ask the GUI to quit"""
        self.app.quit_signal.emit()
        return True

    def kill(self):
        """Forcefully destroy the process, this does not return"""
        os._exit(1)

    def heartbeat(self, port):
        """Tell QML that someone is listening at `port`"""
        self.app.register_heartbeat(port)

    def find_available_port(self, start=first_port):
        """Return the next available port at which a client may listen

        If module "psutil" is available, this also takes into
        account any externally used ports such that no occupied
        port is accidentally used. This is generally recommended.

        Arguments:
            start (int, optional): Port from which to start
                looking, defaults to 6001

        """

        print("Finding available port..")
        occupied_ports = list(self.app.clients)

        try:
            import psutil
            occupied_ports += list(
                c.laddr[-1] for c in psutil.net_connections())
        except ImportError:
            pass

        available = start
        while available in occupied_ports:
            available += 1

        print("Distributing new port %i" % available)
        return available


class CtrlApi(object):
    def __init__(self, ctrl):
        self.ctrl = ctrl


def _server(port, service):
    server = SimpleXMLRPCServer(
        ("127.0.0.1", port),
        allow_none=True,
        logRequests=False)

    server.register_introspection_functions()
    server.register_instance(service)

    return server


def _serve(port, service):
    server = _server(port, service)
    print("Listening on %s:%s" % server.server_address)
    return server.serve_forever()
