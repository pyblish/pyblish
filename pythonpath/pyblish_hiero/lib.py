# Standard library
import os
import sys
import traceback

# Pyblish libraries
import pyblish.api
import pyblish_integration

# Host libraries
import hiero
import PySide

# Local libraries
import plugins

cached_process = None


show = pyblish_integration.show


def setup(console=False):
    """Setup integration
    Registers Pyblish for Hiero plug-ins and appends an item to the File-menu
    Attributes:
        console (bool): Display console with GUI
    """

    def threaded_wrapper(func, *args, **kwargs):
        return hiero.core.executeInMainThreadWithResult(func, *args, **kwargs)

    pyblish_integration.register_python_executable(where("python"))
    pyblish_integration.register_dispatch_wrapper(threaded_wrapper)
    pyblish_integration.setup(console)

    register_plugins()
    add_to_filemenu()
    register_host()

    pyblish_integration.echo("pyblish: Integration loaded..")


def register_host():
    """Register supported hosts"""
    pyblish.api.register_host("hiero")


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
        import pyblish_hiero.lib
        pyblish_hiero.lib.show()
    except Exception:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        message = "".join(traceback.format_exception(
            exc_type, exc_value, exc_traceback))

        sys.stderr.write("Tried launching GUI, but failed.\n")
        sys.stderr.write("Message was: %s\n" % message)
        sys.stderr.write("Publishing in headless mode instead.\n")

        import pyblish.util
        pyblish.util.publish()


def menu_action():
    import pyblish_hiero.lib
    pyblish_hiero.lib.filemenu_publish()


def add_to_filemenu():
    menu_bar = hiero.ui.menuBar()
    file_action = None
    for action in menu_bar.actions():
        if action.text().lower() == 'file':
            file_action = action

    file_menu = file_action.menu()

    action = PySide.QtGui.QAction('Publish', None)
    action.triggered.connect(menu_action)

    hiero.ui.insertMenuAction(action, file_menu, before='Import Clips...')
    action = file_menu.addSeparator()
    hiero.ui.insertMenuAction(action, file_menu, before='Import Clips...')

    # The act of initialising the action adds it to the right-click menu...
    SelectedShotAction = PublishAction()

    # And to enable the Ctrl/Cmd+Alt+C, add it to the Menu bar Edit menu...
    editMenu = hiero.ui.findMenuAction("Edit")
    editMenu.menu().addAction(SelectedShotAction)


class PublishAction(PySide.QtGui.QAction):
    def __init__(self):
        PySide.QtGui.QAction.__init__(self, "Publish", None)
        self.triggered.connect(self.publish)

        for interest in ["kShowContextMenu/kTimeline",
                         "kShowContextMenukBin",
                         "kShowContextMenu/kSpreadsheet"]:
            hiero.core.events.registerInterest(interest, self.eventHandler)

        self.setShortcut("Ctrl+Alt+P")

    def publish(self):
        import pyblish_hiero.lib
        pyblish_hiero.lib.filemenu_publish()

    def eventHandler(self, event):

        # Add the Menu to the right-click menu
        event.menu.addAction(self)
