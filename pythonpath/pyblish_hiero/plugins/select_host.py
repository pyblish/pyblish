import pyblish.api


class SelectHost(pyblish.api.Selector):
    """Inject the host into context"""

    version = (0, 1, 0)

    def process(self, context):
        context.set_data("host", pyblish.api.current_host())
