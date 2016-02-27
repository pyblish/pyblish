import pyblish.api

import hiero


class SelectCurrentFile(pyblish.api.Selector):
    """Inject the current working file into context"""

    version = (0, 1, 0)

    def process(self, context):
        """Todo, inject the current working file"""

        project = context.data('activeProject')
        context.set_data('currentFile', value=project.path())
