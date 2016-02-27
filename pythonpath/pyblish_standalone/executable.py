import time
import socket

import pyblish.api
import pyblish_integration.lib


def start():
    """Start Pyblish QML"""

    pyblish.api.register_host("standalone")
    pyblish_integration.setup()

    max_tries = 5
    while True:
        try:
            time.sleep(0.5)
            pyblish_integration.show()
        except socket.error as e:
            if max_tries <= 0:
                raise Exception("Couldn't run Pyblish QML: %s" % e)
            else:
                print("%s tries left.." % max_tries)
                max_tries -= 1
        else:
            break

    print("Launching Pyblish..")


def stop():
    """Hide Pyblish QML"""
    pyblish_integration.lib.proxy.hide()
