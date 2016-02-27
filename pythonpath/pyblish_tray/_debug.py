import threading


def d1(self):
    import time
    import random
    import itertools

    messages = itertools.cycle([
        "DEBUG..",
        "Launching Pyblish QML..",
        "Finished",
        "Listening for output..",
        "Launching virtual host..",
        "Starting Pyblish..",
        "Spent 132.00 ms creating the application",
        "Entering state: \"hidden\"",
        "Entering state: \"ready\"",
        "Entering state: \"clean\"",
        "Listening on 127.0.0.1:9090",
        "Entering state: \"alive\"",
        "Finding available port..",
        "Distributing new port 9001",
        "Polishing: 149ms",
    ])

    def reader():
        while True:
            self.broadcast(messages.next())
            time.sleep(random.random() * 1)

    t = threading.Thread(target=reader)
    t.daemon = True
    t.start()

    self.broadcast("Starting in debug mode")


def bootstrap(application):
    """Prevent application from launching a subprocess and server"""

    # Mock heavy externals
    application.launch = lambda: d1(application)
    application.launch_virtual_host = lambda: True

    # Mock calls during clean-up
    application._vhost_ctrl.server = type(
        "DebugServer", (object,), {"shutdown": lambda self: True})()
    application._popen = type(
        "DebugPopen", (object,), {"kill": lambda self: True})()

    application.broadcast("Application bootstrapped")
