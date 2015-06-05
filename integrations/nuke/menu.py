"""Wrapper for Pyblish Nuke integration"""

import os
import sys
import pyblish_nuke

package_dir = os.path.dirname(pyblish_nuke.__file__)
integration_dir = os.path.join(package_dir, "nuke_path")

sys.path.insert(0, integration_dir)

from menu import *
