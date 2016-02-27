import pyblish.api

import hiero


class CollectActiveProject(pyblish.api.Collector):
    """Inject the active project into context"""

    version = (0, 1, 0)
    order = pyblish.api.Collector.order - 0.1

    def process(self, context):

        context.set_data('activeProject', value=hiero.activeProject)
