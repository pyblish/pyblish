"""Pyblish QML command-line interface"""

import sys
import argparse

from . import app


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true")

    args = parser.parse_args()

    return app.main(debug=args.debug)


sys.exit(cli())
