import os
import imp

util = imp.load_source("__pyblish_util", os.path.realpath(os.path.join(__file__, "..", "..", "__pyblish_util.py")))
util.wrap_module(__name__)
