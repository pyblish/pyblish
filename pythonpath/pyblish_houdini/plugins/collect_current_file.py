import pyblish.api

import hou


class CollectCurrentFile(pyblish.api.ContextPlugin):
    """Inject the current working file into context

    .. note:: This plug-in is implemented in all relevant host integrations

    """

    label = "Current File"
    hosts = ['houdini']
    order = pyblish.api.CollectorOrder
    version = (0, 1, 0)

    def process(self, context):
        """inject the current working file"""
        current_file = hou.hipFile.path()
        context.data['currentFile'] = current_file
