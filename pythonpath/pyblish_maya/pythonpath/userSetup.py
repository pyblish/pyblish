
try:
    __import__("pyblish_maya")

except ImportError as e:
    import traceback
    print ("pyblish-maya: Could not load integration: %s"
           % traceback.format_exc())

else:
    import pyblish_maya
    pyblish_maya.setup()
