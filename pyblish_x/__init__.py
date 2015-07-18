import os
import sys


def install():
    pythonpath = os.path.join(__file__, "..", "..", "pythonpath")
    sys.path.insert(0, os.path.realpath(pythonpath))
