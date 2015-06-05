try:
    __import__("pyblish_houdini")

except ImportError as e:
    print "pyblish: Could not load integration: %s" % e

else:
    import pyblish_houdini
    pyblish_houdini.setup()
