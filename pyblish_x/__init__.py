import os
import sys


def install():
    pythonpath = os.path.join(__file__, "..", "..", "python")
    sys.path.insert(0, os.path.realpath(pythonpath))
