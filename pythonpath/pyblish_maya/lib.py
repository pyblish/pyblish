# Standard library
import os
import sys
import inspect
import contextlib

# Pyblish libraries
import pyblish
import pyblish.api

# Host libraries
from maya import mel
from maya import cmds
from maya import utils

# Local libraries
import plugins

self = sys.modules[__name__]
self._has_been_setup = False

try:
    import pyblish_integration
    self._has_integration = True
except:
    self._has_integration = False


def show():
    if self._has_integration:
        return pyblish_integration.show()
    else:
        return sys.stderr.write("GUI requires pyblish-integration.\n")

def setup(console=False, port=None):
    """Setup integration

    Registers Pyblish for Maya plug-ins and appends an item to the File-menu

    Attributes:
        console (bool): Display console with GUI
        port (int, optional): Port from which to start looking for an
            available port to connect with Pyblish QML, default
            provided by Pyblish Integration.

    """

    if self._has_been_setup:
        teardown()

    if self._has_integration:
        def threaded_wrapper(func, *args, **kwargs):
            return utils.executeInMainThreadWithResult(func, *args, **kwargs)

        pyblish_integration.register_dispatch_wrapper(threaded_wrapper)
        pyblish_integration.setup(console=console, port=port)

    register_plugins()
    add_to_filemenu()
    register_host()

    self._has_been_setup = True
    sys.stdout.write("pyblish: Integration loaded..")


def teardown():
    """Remove integration"""
    if not self._has_been_setup:
        return

    if self._has_integration:
        pyblish_integration.teardown()

    deregister_plugins()
    deregister_host()
    remove_from_filemenu()

    self._has_been_setup = False
    sys.stdout.write("pyblish: Integration torn down successfully")


def deregister_plugins():
    # Register accompanying plugins
    plugin_path = os.path.dirname(plugins.__file__)
    pyblish.api.deregister_plugin_path(plugin_path)
    sys.stdout.write("pyblish: Deregistered %s" % plugin_path)


def register_host():
    """Register supported hosts"""
    pyblish.api.register_host("mayabatch")
    pyblish.api.register_host("mayapy")
    pyblish.api.register_host("maya")

def deregister_host():
    """Register supported hosts"""
    pyblish.api.deregister_host("mayabatch")
    pyblish.api.deregister_host("mayapy")
    pyblish.api.deregister_host("maya")


def register_plugins():
    # Register accompanying plugins
    plugin_path = os.path.dirname(plugins.__file__)
    pyblish.api.register_plugin_path(plugin_path)
    sys.stdout.write("pyblish: Registered %s" % plugin_path)


def add_to_filemenu(gui=True):
    """Add Pyblish to file-menu

    .. note:: We're going a bit hacky here, probably due to my lack
        of understanding for `evalDeferred` or `executeDeferred`,
        so if you can think of a better solution, feel free to edit.

    """

    if hasattr(cmds, 'about') and not cmds.about(batch=True):
        # As Maya builds its menus dynamically upon being accessed,
        # we force its build here prior to adding our entry using it's
        # native mel function call.
        mel.eval("evalDeferred buildFileMenu")

        # Serialise function into string
        script = inspect.getsource(_add_to_filemenu)
        script += "\n_add_to_filemenu(gui=%s)" % gui

        # If cmds doesn't have any members, we're most likely in an
        # uninitialized batch-mode. It it does exists, ensure we
        # really aren't in batch mode.
        cmds.evalDeferred(script)


def remove_from_filemenu():
    for item in ("pyblishOpeningDivider",
                 "pyblishScene",
                 "pyblishCloseDivider"):
        if cmds.menuItem(item, exists=True):
            cmds.deleteUI(item, menuItem=True)


def _add_to_filemenu(gui=True):
    """Helper function for the above :func:add_to_filemenu()

    This function is serialised into a string and passed on
    to evalDeferred above.

    """

    import os
    import pyblish
    from maya import cmds

    # This must be duplicated here, due to this function
    # not being available through the above `evalDeferred`
    for item in ("pyblishOpeningDivider",
                 "pyblishScene",
                 "pyblishCloseDivider"):
        if cmds.menuItem(item, exists=True):
            cmds.deleteUI(item, menuItem=True)

    icon = os.path.dirname(pyblish.__file__)
    icon = os.path.join(icon, "icons", "logo-32x32.svg")

    command = ("import pyblish_maya;pyblish_maya.show()" if gui
               else "import pyblish.util;pyblish.util.publish()")

    print "Adding to menu: %s" % command
    cmds.menuItem("pyblishOpeningDivider",
                  divider=True,
                  insertAfter="saveAsOptions",
                  parent="mainFileMenu")

    cmds.menuItem("pyblishScene",
                  insertAfter="pyblishOpeningDivider",
                  label="Publish",
                  parent="mainFileMenu",
                  image=icon,
                  command=command)

    cmds.menuItem("pyblishCloseDivider",
                  insertAfter="pyblishScene",
                  parent="mainFileMenu",
                  divider=True)


@contextlib.contextmanager
def maintained_selection():
    """Maintain selection during context

    Example:
        >>> with maintained_selection():
        ...     # Modify selection
        ...     cmds.select('node', replace=True)
        >>> # Selection restored

    """

    previous_selection = cmds.ls(selection=True)
    try:
        yield
    finally:
        if previous_selection:
            cmds.select(previous_selection,
                        replace=True,
                        noExpand=True)
        else:
            cmds.select(deselect=True,
                        noExpand=True)


@contextlib.contextmanager
def maintained_time():
    """Maintain current time during context

    Example:
        >>> with maintained_time():
        ...    cmds.playblast()
        >>> # Time restored

    """

    ct = cmds.currentTime(query=True)
    try:
        yield
    finally:
        cmds.currentTime(ct, edit=True)
