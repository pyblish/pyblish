import os
import sys
import inspect

from .version import *


def register_vendor_packages():
    vendor_dir = os.path.join(__file__, "..", "vendor")
    vendor_dir = os.path.realpath(vendor_dir)
    sys.path.insert(0, vendor_dir)

register_vendor_packages()

self = sys.modules[__name__]
self._dispatch_wrapper = None


def register_dispatch_wrapper(wrapper):
    """Register a dispatch wrapper for servers

    The wrapper must have this exact signature:
        (func, *args, **kwargs)

    Usage:
        >>> def wrapper(func, *args, **kwargs):
        ...   return func(*args, **kwargs)
        ...
        >>> register_dispatch_wrapper(wrapper)
        >>> deregister_dispatch_wrapper()

    """

    signature = inspect.getargspec(wrapper)
    if (len(signature.args) != 1
            or signature.varargs is None
            or signature.keywords is None):
        raise TypeError("Wrapper signature mismatch")

    self._dispatch_wrapper = wrapper


def deregister_dispatch_wrapper():
    self._dispatch_wrapper = None


def dispatch_wrapper():
    return self._dispatch_wrapper
