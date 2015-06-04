import os
import sys


def wrap_module(module):
    """Wrap `module` into corresponding module from Pyblish X

    Arguments:
        module (str): Name of module, e.g. "pyblish"

    """

    library_dir = os.path.join(__file__, "..", "..", "modules", module)
    library_dir = os.path.realpath(library_dir)

    assert os.path.isdir(library_dir), library_dir

    if library_dir not in sys.path:
        sys.path.insert(0, library_dir)

    module = module.replace("-", "_")
    mod = __import__(module)
    sys.modules[module] = mod
    reload(mod)


def augment_pythonpath():
    """Add Pyblish packages to PYTHONPATH"""
    python_dir = os.path.join(__file__, "..", "..")
    python_dir = os.path.realpath(python_dir)

    if python_dir not in os.environ["PYTHONPATH"]:
        var = python_dir + os.pathsep + os.environ.get("PYTHONPATH", "")
        os.environ["PYTHONPATH"] = var
