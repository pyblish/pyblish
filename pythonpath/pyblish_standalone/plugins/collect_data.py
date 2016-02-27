import os
import pyblish.api
import pyblish_standalone


class CollectData(pyblish.api.Collector):
    """Collects data passed from via CLI"""

    order = pyblish.api.Collector.order - 0.1

    def process(self, context):
        self.log.info("Adding data from command-line into Context..")

        kwargs = pyblish_standalone.kwargs.copy()
        fname = os.path.abspath(kwargs.get("file"))
        self.log.info("Adding filename: %s" % fname)
        context.set_data("currentFile", fname)

        data = dict(kwargs.get("data") or {})
        for key, value in data.iteritems():
            self.log.info("%s = %s" % (key, value))
            context.set_data(key, value)
