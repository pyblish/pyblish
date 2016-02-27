"""Internal library for Pyblish Maya

Attributes:
    CREATE_NO_WINDOW: Flag from MSDN;
        https://msdn.microsoft.com/en-us/library/ms684863(v=VS.85).aspx
    PYBLISH_QML_CONSOLE: Environment variable for displaying
        the console upon launching Pyblish QML

"""

# Standard library
import os
import sys
import time
import socket
import logging
import threading
import traceback
import subprocess

import pyblish_rpc
import pyblish_rpc.server
import pyblish_qml
import pyblish_qml.client
import pyblish_qml.server
import pyblish.api

CREATE_NO_WINDOW = 0x08000000
PYBLISH_QML_CONSOLE = "PYBLISH_QML_CONSOLE"
PYBLISH_QML_FIRST_PORT = "PYBLISH_QML_FIRST_PORT"
PYBLISH_CLIENT_PORT = "PYBLISH_CLIENT_PORT"

log = logging.getLogger("pyblish-integration")

self = sys.modules[__name__]
self.proxy = None
self.port = None
self.executable = None


def show(port=None):
    """Show the Pyblish graphical user interface

    An interface may already have been loaded; if that's the
    case, we favour it to launching a new unless `prefer_cached`
    is False.

    Arguments:
        port (int, optional): Port at which host is listening, defaults
            to the one obtained through :func:`setup()`. Note that passing
            in a custom port can lead to unexpected behaviour, such as
            showing a QML window for another host.

    """

    port = port or self.port

    if port is None:
        raise TypeError("Integration not initialised correctly")

    if self.proxy is None:
        self.proxy = pyblish_qml.client.proxy()

    settings = pyblish_qml.settings.to_dict()

    try:
        self.proxy.show(port, settings)

    except (socket.error, socket.timeout):
        _preload()
        self.proxy.show(port, settings)


def setup(console=False, port=None):
    """Setup integration

    Find or launch Pyblish QML and setup endpoint in host
    for it to communicate with. Once setup is complete,
    call :func:`show` to display the GUI.

    Attributes:
        console (bool): Display console with GUI
        port (int, optional): Port from which to start
            looking for available ports, defaults to
            pyblish_qml.server.first_port

    """

    if console:
        os.environ[PYBLISH_QML_CONSOLE] = "1"

    register_callbacks()

    try:
        # In case QML is live and well, ask it
        # for the next available port number.
        args = [port] if port else []
        self.proxy = pyblish_qml.client.proxy()
        self.port = self.proxy.find_available_port(*args)

    except (socket.timeout, socket.error):
        # Otherwise, we can assume that this is
        # the first time QML is being opened.
        self.port = port or pyblish_qml.server.first_port
        popen = _preload()

        assert popen.poll() is None

    finally:
        os.environ[PYBLISH_CLIENT_PORT] = str(self.port)

        try:
            _serve(self.port)
            log.debug("Integration successful!")

        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            message = "".join(traceback.format_exception(
                exc_type, exc_value, exc_traceback))
            log.debug(message)
            log.debug("Integration failed..")


def teardown():
    """Tear down integration"""
    del self.proxy
    self.port = None
    self.proxy = None
    pyblish_rpc.server.kill()
    echo("Integration torn down successfully")


def _serve(port):
    def server():
        """Provide QML with a friend to speak with"""
        self.server = pyblish_rpc.server.start_production_server(port)

    def heartbeat_emitter():
        """Let QML know we're still here"""
        proxy = pyblish_qml.client.proxy()

        while True:
            try:
                proxy.heartbeat(port)
                time.sleep(1)
            except (socket.error, socket.timeout):
                pass

    for worker in (server, heartbeat_emitter):
        t = threading.Thread(target=worker, name=worker.__name__)
        t.daemon = True
        t.start()

    log.debug("Server running @ %i" % port)

    return port


def _preload(port=None):
    """Load an instance of Pyblish QML in the background

    Arguments:
        port (int, optional): Port at which QML will be listening

    Usage:
        The preloaded Pyblish QML can be accessed through
        :func:`pyblish_qml.client.proxy()`, which opens up
        an XMLRPC connection through which commands may be sent,
        such as :func:`p.find_available_port()`.

    """

    console = True if os.environ.get(PYBLISH_QML_CONSOLE) else False
    executable = registered_python_executable() or "python"
    kwargs = {
        "args": [executable, "-m", "pyblish_qml"],
        "creationflags": (
            CREATE_NO_WINDOW
            if os.name == "nt" and not console
            else 0
        )
    }

    if port is not None:
        kwargs["args"] += ["--port", str(port)]

    return subprocess.Popen(**kwargs)


def register_callbacks():
    def toggle_instance(instance, new_value, old_value):
        instance.data["publish"] = new_value

    pyblish.api.register_callback("instanceToggled", toggle_instance)


def register_dispatch_wrapper(wrapper):
    pyblish_rpc.register_dispatch_wrapper(wrapper)


def register_python_executable(executable):
    self.executable = executable


def registered_python_executable():
    return self.executable


def echo(text):
    print(text)
