import logging

import nuke

logging.basicConfig(level=logging.INFO)

try:
    __import__("pyblish_nuke")
    __import__("pyblish")

except ImportError as e:
    nuke.tprint("pyblish: Could not load integration: %s " % e)

else:

    import pyblish_nuke.lib

    # Setup integration
    pyblish_nuke.lib.setup()
