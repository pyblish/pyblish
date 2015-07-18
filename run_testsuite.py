import os
import sys
import nose
import mock

sys.modules["maya"] = mock.MagicMock()
sys.modules["nuke"] = mock.MagicMock()
sys.modules["hou"] = mock.MagicMock()
sys.modules["hdefereval"] = mock.MagicMock()

# Expose Pyblish X to PYTHONPATH
path = os.path.dirname(__file__)
sys.path.insert(0, path)

if __name__ == '__main__':
    argv = sys.argv[:]
    argv.extend(['--include=tests', '--verbose'])
    nose.main(argv=argv)
