import os
import sys
import time
import socket
import argparse

import executable
import pyblish_standalone


def cli():
    parser = argparse.ArgumentParser(prog="pyblish_standalone")

    parser.add_argument("file", nargs="?",
                        help="Pass file to Context as `currentFile`")
    parser.add_argument("-d", "--data", nargs=2, action="append",
                        metavar=("key", "value"),
                        help=("Append data to context, "
                              "can be called multiple times"))
    parser.add_argument("--path", action="append",
                        help=("Append path to PYBLISHPLUGINPATH, "
                              "can be called multiple times"))

    kwargs = parser.parse_args(sys.argv[1:])

    # Store reference to keyword arguments, for Collection
    pyblish_standalone.kwargs = kwargs.__dict__

    plugins_path = os.path.join(os.path.dirname(__file__), "plugins")

    pyblish_path = os.environ.get("PYBLISHPLUGINPATH", "").split(os.pathsep)
    pyblish_path.append(plugins_path)
    pyblish_path.extend(kwargs.path or [])

    os.environ["PYBLISHPLUGINPATH"] = os.pathsep.join(pyblish_path)

    executable.start()


if __name__ == "__main__":
    cli()
    print("Press Ctrl-C to quit..")

    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        # Close GUI on terminal session end
        try:
            executable.stop()
        except socket.error:
            # QML client closed before host? No problem.
            pass
