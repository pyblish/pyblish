import sys
import traceback

import hiero

try:
    __import__("pyblish_hiero")
    __import__("pyblish")

except ImportError as e:
    print traceback.format_exc()
    print("pyblish: Could not load integration: %s " % e)

else:

    import pyblish_hiero.lib

    # Setup integration
    pyblish_hiero.lib.setup()
