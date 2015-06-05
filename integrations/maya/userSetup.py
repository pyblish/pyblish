"""Wrapper for Pyblish Maya integration"""

import os
import sys
import pyblish_maya

package_dir = os.path.dirname(pyblish_maya.__file__)
integration_dir = os.path.join(package_dir, "pythonpath")

sys.path.insert(0, integration_dir)

from userSetup import *
