import traceback

try:
    __import__("pyblish_hiero")
    __import__("pyblish")

except ImportError as e:
    print traceback.format_exc()
    print("pyblish: Could not load integration: %s " % e)

else:
    # Setup integration
    import pyblish_hiero.lib
    pyblish_hiero.lib.setup()
