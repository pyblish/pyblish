#!/usr/bin/env bash
export packages=pyblish-base \
                pyblish-hiero \
                pyblish-houdini \
                pyblish-integration \
                pyblish-maya \
                pyblish-nuke \
                pyblish-qml \
                pyblish-rpc \
                pyblish-standalone \
                pyblish-tray
python dist.py $(pwd)\pythonpath "$packages" --clean