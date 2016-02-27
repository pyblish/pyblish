"""Pyblish QML command-line interface"""

import sys
import argparse

from . import app


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="Python",
                        help="deprecated")
    parser.add_argument("--port", type=int, default=6000, help="deprecated")
    parser.add_argument("--pid", type=int, default=None, help="deprecated")
    parser.add_argument("--preload", action="store_true", help="deprecated")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--validate", action="store_true")

    kwargs = parser.parse_args()
    debug = kwargs.debug
    validate = kwargs.validate

    return app.main(debug=debug,
                    validate=validate)


sys.exit(cli())
