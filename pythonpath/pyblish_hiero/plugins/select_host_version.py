import pyblish.api

import hiero


class SelectHostVersion(pyblish.api.Selector):
    """Inject the hosts version into context"""

    version = (0, 1, 0)

    def process(self, context):
        version_name = '%s.%s%s' % (hiero.core.env['VersionMajor'],
                                    hiero.core.env['VersionMinor'],
                                    hiero.core.env['VersionRelease'])

        context.set_data('hostVersion', value=version_name)
