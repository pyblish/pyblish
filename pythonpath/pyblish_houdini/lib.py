# Standard library
import os
import contextlib

# Pyblish libraries
import pyblish.api
import pyblish_integration

# Host libraries
import hou
import hdefereval

# Local libraries
import plugins

show = pyblish_integration.show


def setup(console=False, port=None):
    """Setup integration

    Registers Pyblish for Maya plug-ins and appends an item to the File-menu

    Attributes:
        preload (bool): Preload the current GUI
        console (bool): Display console with GUI

    """

    def threaded_wrapper(func, *args, **kwargs):
        return hdefereval.executeInMainThreadWithResult(func, *args, **kwargs)

    pyblish_integration.register_dispatch_wrapper(threaded_wrapper)
    pyblish_integration.setup(console=console, port=port)

    register_host()
    register_plugins()

    pyblish_integration.echo("pyblish: Integration loaded..")


def register_host():
    """Register supported hosts"""
    pyblish.api.register_host("hpython")
    pyblish.api.register_host("houdini")


def register_plugins():
    # Register accompanying plugins
    plugin_path = os.path.dirname(plugins.__file__)
    pyblish.api.register_plugin_path(plugin_path)
    pyblish_integration.echo("pyblish: Registered %s" % plugin_path)


@contextlib.contextmanager
def maintained_selection():
    """Maintain selection during context

    Example:
        >>> with maintained_selection():
        ...     # Modify selection
        ...     node.setSelected(on=False, clear_all_selected=True)
        >>> # Selection restored

    """

    previous_selection = hou.selectedNodes()
    try:
        yield
    finally:
        if previous_selection:
            for node in previous_selection:
                node.setSelected(on=True)
        else:
            for node in previous_selection:
                node.setSelected(on=False)
