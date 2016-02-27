# Standard library
import os
import sys
import traceback

# Pyblish libraries
import pyblish.api
import pyblish_integration

# Host libraries
import nuke

# Local libraries
import plugins

cached_process = None


def show():
    pyblish_integration.show()


def setup(console=False, port=None):
    """Setup integration

    Registers Pyblish for Maya plug-ins and appends an item to the File-menu

    Attributes:
        preload (bool): Preload the current GUI
        console (bool): Display console with GUI

    """

    if not os.name == "nt":
        return pyblish_integration.echo("Sorry, integration only"
                                        "supported on Windows.")

    def threaded_wrapper(func, *args, **kwargs):
        return nuke.executeInMainThreadWithResult(func, args, kwargs)

    pyblish_integration.register_python_executable(where("python"))
    pyblish_integration.register_dispatch_wrapper(threaded_wrapper)
    pyblish_integration.setup(console=console, port=port)

    register_plugins()
    register_host()
    add_to_filemenu()

    pyblish_integration.echo("pyblish: Integration loaded..")


def register_host():
    """Register supported hosts"""
    pyblish.api.register_host("nuke")


def register_plugins():
    # Register accompanying plugins
    plugin_path = os.path.dirname(plugins.__file__)
    pyblish.api.register_plugin_path(plugin_path)
    pyblish_integration.echo("pyblish: Registered %s" % plugin_path)


def where(program):
    """Parse PATH for executables

    Windows note:
        PATHEXT yields possible suffixes, such as .exe, .bat and .cmd

    Usage:
        >>> where("python")
        c:\python27\python.exe

    """

    suffixes = [""]

    try:
        # Append Windows suffixes, such as .exe, .bat and .cmd
        suffixes.extend(os.environ.get("PATHEXT").split(os.pathsep))
    except:
        pass

    for path in os.environ["PATH"].split(os.pathsep):

        # A path may be empty.
        if not path:
            continue

        for suffix in suffixes:
            full_path = os.path.join(path, program + suffix)
            if os.path.isfile(full_path):
                return full_path


def filemenu_publish():
    """Add Pyblish to file-menu"""

    try:
        import pyblish_nuke.lib
        pyblish_nuke.lib.show()
    except Exception:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        message = "".join(traceback.format_exception(
            exc_type, exc_value, exc_traceback))

        sys.stderr.write("Tried launching GUI, but failed.\n")
        sys.stderr.write("Message was: %s\n" % message)
        sys.stderr.write("Publishing in headless mode instead.\n")

        import pyblish.util
        pyblish.util.publish()


def add_to_filemenu():
    menubar = nuke.menu('Nuke')
    menu = menubar.menu('File')

    menu.addSeparator(index=8)

    cmd = 'import pyblish_nuke.lib;pyblish_nuke.lib.filemenu_publish()'
    menu.addCommand('Publish', cmd, index=9)

    menu.addSeparator(index=10)
