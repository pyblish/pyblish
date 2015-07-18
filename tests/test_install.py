
def test_install():
    import pyblish_x
    pyblish_x.install()

    __import__("pyblish")
    __import__("pyblish_maya")
    __import__("pyblish_houdini")
    __import__("pyblish_nuke")
    __import__("pyblish_qml")
    __import__("pyblish_rpc")
    __import__("pyblish_integration")
