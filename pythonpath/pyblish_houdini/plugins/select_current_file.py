import pyblish.api

import hou


@pyblish.api.log
class SelectCurrentFile(pyblish.api.Selector):
    """Inject the current working file into context

    .. note:: This plug-in is implemented in all relevant host integrations

    """

    hosts = ['houdini']
    version = (0, 1, 0)

    def process(self, context):
        """Todo, inject the current working file"""
        current_file = hou.hipFile.path()
        context.set_data('currentFile', value=current_file)
