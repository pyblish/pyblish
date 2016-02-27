import os
import sys
import warnings

try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser

import xml.etree.ElementTree as ElementTree

cwd = os.path.dirname(sys.executable)
qtconf_path = os.path.join(cwd, "qt.conf")


error_message = {
    "qtquick2plugin.dll": (
        "Could not load Qt binaries. Make sure you have only"
        "one copy of the binaries on your PATH"
    )
}


def validate():
    """Validate compatibility with environment and Pyblish QML"""

    errors = dict()
    for test in (test_architecture,
                 test_pyqt_availability,
                 test_pyblish_availability,
                 test_qtconf_availability,
                 test_qtconf_correctness,
                 test_qt_availability):
        try:
            test()
        except Exception as e:
            errors[test] = e

    if not errors:
        print("=" * 78)
        print()
        print(""" - Success!

{exe} is well suited to run Pyblish QML""".format(exe=sys.executable))
        print()
        print("=" * 78)

        return True

    print("=" * 78)
    print()
    print(" - Failed")
    print()
    for test, error in errors.iteritems():
        print(test.__name__)
        print("    %s" % error)
    print()
    print("=" * 78)

    return False


def test_architecture():
    """Is the Python interpreter 64-bit?"""
    if not sys.maxsize > 2**32:
        raise Exception("32-bit interpreter detected; must be running "
                        "Python x86-64\nE.g. https://www.python.org/ftp"
                        "/python/2.7.9/python-2.7.9.amd64.msi")


def test_pyqt_availability():
    """Is PyQt5 available?"""
    try:
        __import__("PyQt5")
    except:
        raise Exception("PyQt5 not found")


def test_pyblish_availability():
    """Is Pyblish available?"""
    try:
        __import__("pyblish")
        __import__("pyblish_qml")
        __import__("pyblish_rpc")
    except:
        raise Exception("Pyblish not found")


def test_qtconf_availability():
    """Is there a qt.conf?"""
    if not os.path.isfile(qtconf_path):
        raise Exception("No qt.conf found at %s" % cwd)


def test_qtconf_correctness():
    """Is the qt.conf correctly configured?"""
    config = ConfigParser.ConfigParser()
    config.read(qtconf_path)

    prefix_dir = config.get("Paths", "prefix")

    try:
        binaries_dir = config.get("Paths", "binaries")
    except:
        binaries_dir = prefix_dir

    assert binaries_dir == prefix_dir, (
        "qt.conf misconfigured, binaries not in prefix directory")
    assert os.path.isdir(os.path.abspath(prefix_dir)), (
        "qt.conf misconfigured, prefix directory is not a directory")
    assert prefix_dir.endswith("PyQt5"), (
        "qt.conf misconfigured, prefix should end with PyQt5")

    if os.name == "nt":
        assert "designer.exe" in os.listdir(prefix_dir), (
            "qt.conf misconfigured, designer.exe was missing "
            "(and possibly others)")


def test_qt_availability():
    """If Qt is installed, is it the right version?"""
    if os.name == "nt" and os.path.exists(r"c:\Qt"):
        print("Qt detected..")

        path = r"c:\Qt\components.xml"

        try:
            with open(path) as f:
                components = xml_to_dict(f.read())

            package = None
            for p in components["Package"]:
                if p["Name"] == "qt.54":
                    package = p

            if package is None:
                raise TypeError("Qt detected; but version != 5.4")

            PyQt5 = __import__("PyQt5")
            version = package["Version"].rsplit("-", 1)[0]
            if not version == PyQt5.qt_version:
                raise TypeError("Qt detected; but there was a "
                                "version mismatch: Qt = {qt} | "
                                "PyQt5 = {pyqt}".format(
                                    qt=version,
                                    pyqt=PyQt5.qt_version))

        except TypeError:
            raise

        except:
            warnings.warn("Qt detected; ensure it matches the "
                          "version used to compile PyQt5")


def generate_safemode_windows():
    """Produce batch file to run QML in safe-mode

    Usage:
        $ python -c "import compat;compat.generate_safemode_windows()"
        $ run.bat

    """

    try:
        import pyblish
        import pyblish_qml
        import pyblish_endpoint
        import PyQt5

    except ImportError:
        print("Run this in a terminal with access to the Pyblish libraries and PyQt5")
        return

    template = r"""@echo off

    :: Clear all environment variables

    @echo off
    if exist ".\backup_env.bat" del ".\backup_env.bat"
    for /f "tokens=1* delims==" %%a in ('set') do (
    echo set %%a=%%b>> .\backup_env.bat
    set %%a=
    )

    :: Set only the bare essentials

    set PATH={PyQt5}
    set PATH=%PATH%;{python}
    set PYTHONPATH={pyblish}
    set PYTHONPATH=%PYTHONPATH%;{pyblish_qml}
    set PYTHONPATH=%PYTHONPATH%;{pyblish_endpoint}
    set PYTHONPATH=%PYTHONPATH%;{PyQt5}

    set SystemRoot=C:\Windows

    :: Run Pyblish

    python -m pyblish_qml

    :: Restore environment
    backup_env.bat

    """

    values = {}
    for lib in (pyblish, pyblish_qml, pyblish_endpoint, PyQt5):
        values[lib.__name__] = os.path.dirname(os.path.dirname(lib.__file__))

    values["python"] = os.path.dirname(sys.executable)

    with open("run.bat", "w") as f:
        print("Writing %s" % template.format(**values))
        f.write(template.format(**values))


def xml_to_dict(xml):
    """Convert XML document into Python dictionary

    Arguments:
        xml (str): Xml document to convert

    """

    root = ElementTree.XML(xml)
    return XmlDictConfig(root)


class XmlListConfig(list):
    def __init__(self, aList):
        for element in aList:
            if element:
                # treat like dict
                if len(element) == 1 or element[0].tag != element[1].tag:
                    self.append(XmlDictConfig(element))
                # treat like list
                elif element[0].tag == element[1].tag:
                    self.append(XmlListConfig(element))
            elif element.text:
                text = element.text.strip()
                if text:
                    self.append(text)


class XmlDictConfig(dict):
    """Convert XML to Python dictionary

    Example:
        >> tree = ElementTree.parse('your_file.xml')
        >> root = tree.getroot()
        >> xmldict = XmlDictConfig(root)

        Or, if you want to use an XML string:

        >> root = ElementTree.XML(xml_string)
        >> xmldict = XmlDictConfig(root)

        And then use xmldict for what it is... a dict.

    """

    def __init__(self, parent_element):
        if parent_element.items():
            self.updateShim(dict(parent_element.items()))
        for element in parent_element:
            if len(element):
                aDict = XmlDictConfig(element)
                if element.items():
                    aDict.updateShim(dict(element.items()))
                self.updateShim({element.tag: aDict})
            elif element.items():
                self.updateShim({element.tag: dict(element.items())})
            elif element.text is not None:
                self.updateShim({element.tag: element.text.strip()})

    def updateShim(self, aDict):
        for key in aDict.keys():
            if key in self:
                value = self.pop(key)
                if type(value) is not list:
                    listOfDicts = []
                    listOfDicts.append(value)
                    listOfDicts.append(aDict[key])
                    self.update({key: listOfDicts})

                else:
                    value.append(aDict[key])
                    self.update({key: value})
            else:
                self.update(aDict)


def windows_taskbar_compat():
    """Enable icon and taskbar grouping for Windows 7+"""

    import ctypes
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(u"pyblish.qml")


def main():
    if os.name == "nt":
        windows_taskbar_compat()


if __name__ == '__main__':
    validate()
