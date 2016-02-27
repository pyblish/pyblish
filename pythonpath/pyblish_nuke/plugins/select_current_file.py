import os

import pyblish.api

import nuke


@pyblish.api.log
class SelectCurrentFile(pyblish.api.Selector):
    """Inject the current working file into context"""

    hosts = ['nuke']
    version = (0, 1, 0)

    def process(self, context):
        """Todo, inject the current working file"""
        current_file = nuke.root().name()

        # Maya returns forward-slashes by default
        normalised = os.path.normpath(current_file)

        context.set_data('current_file', value=normalised)
        context.set_data('currentFile', value=normalised)
