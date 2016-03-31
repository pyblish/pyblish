"""Client communication library

This library is responsible for intercepting and processing
both incoming and outgoing communication. Incoming communication
is parsed into "Object Proxys" (see below) whereas outgoing
communication is serialised back into its original JSON.

"""

import socket

try:
    import httplib
except ImportError:
    # Python 3
    import http.client as httplib

try:
    import xmlrpclib
except ImportError:
    # Python 3
    import xmlrpc.server as xmlrpclib


import pyblish.api
import pyblish.plugin


class Proxy(object):
    """Wrap ServerProxy with logic and object proxies

    The proxy mirrors the remote interface to provide an
    as-similar experience as possible.

    """

    _instance = None

    def __getattr__(self, attr):
        """Any call not overloaded, simply pass it on"""
        return getattr(self._proxy, attr)

    def __init__(self, port, user=None, password=None):
        self.cached_context = list()
        self.cached_discover = list()

        transport = TimeoutTransport()

        self._proxy = xmlrpclib.ServerProxy(
            "http://{auth}127.0.0.1:{port}/pyblish".format(
                port=port,
                auth=("{user}:{pwd}@".format(
                    user=user, pwd=password)
                ) if user else ""),
            allow_none=True,
            transport=transport)

    def test(self, **vars):
        """Vars can only be passed as a non-keyword argument"""
        return self._proxy.test(vars)

    def ping(self):
        """Convert Fault to True/False"""
        try:
            self._proxy.ping()
        except (socket.timeout, socket.error):
            return False
        return True

    def process(self, plugin, context, instance=None, action=None):
        """Transmit a `process` request to host

        Arguments:
            plugin (PluginProxy): Plug-in to process
            context (ContextProxy): Filtered context
            instance (InstanceProxy, optional): Instance to process
            action (str, optional): Action to process

        """

        plugin = plugin.to_json()
        instance = instance.to_json() if instance is not None else None
        return self._proxy.process(plugin, instance, action)

    def repair(self, plugin, context, instance=None):
        plugin = plugin.to_json()
        instance = instance.to_json() if instance is not None else None
        return self._proxy.repair(plugin, instance)

    def context(self):
        self.cached_context = ContextProxy.from_json(self._proxy.context())
        return self.cached_context

    def discover(self):
        self.cached_discover[:] = list()
        for plugin in self._proxy.discover():
            self.cached_discover.append(PluginProxy.from_json(plugin))

        return self.cached_discover

    def emit(self, signal, **kwargs):
        self._proxy.emit(signal, kwargs)


class TimeoutTransport(xmlrpclib.Transport):
    """Some requests may take a very long time, and that is ok"""
    timeout = 60 * 60  # 1 hour

    def make_connection(self, host):
        h = HttpWithTimeout(host, timeout=self.timeout)
        return h


class HttpWithTimeout(httplib.HTTP):
    def __init__(self, host="", port=None, strict=None, timeout=5.0):
        self._setup(self._connection_class(
            host,
            port if port != 0 else None,
            strict,
            timeout=timeout)
        )

    def getresponse(self, *args, **kw):
        return self._conn.getresponse(*args, **kw)


# Object Proxies


class ContextProxy(pyblish.api.Context):
    """Context Proxy

    Given a JSON-representation of a Context, emulate its interface.

    """

    def create_instance(self, name, **kwargs):
        instance = InstanceProxy(name, parent=self)
        instance.data.update(kwargs)
        return instance

    @classmethod
    def from_json(cls, context):
        self = cls()

        for instance in context["children"]:
            instance = InstanceProxy.from_json(instance)
            self.add(instance)

        self.data = context.get("data", {})
        self.data["pyblishClientVersion"] = pyblish.api.version

        return self

    def to_json(self):
        return {
            "children": list(self),
            "data": self.data
        }


class InstanceProxy(pyblish.api.Instance):
    """Instance Proxy

    Given a JSON-representation of an Instance, emulate its interface.

    """

    @classmethod
    def from_json(cls, instance):
        self = cls(instance["name"])
        copy = instance.copy()
        copy["data"] = copy.pop("data")
        self.__dict__.update(copy)
        self[:] = instance["children"]
        return self

    def to_json(self):
        return {
            "name": self.name,
            "id": self.id,
            "data": self.data,
            "children": list(self),
        }


class PluginProxy(object):
    """Plug-in Proxy

    Given a JSON-representation of an Plug-in, emulate its interface.

    """

    @classmethod
    def from_json(cls, plugin):
        """Build PluginProxy object from incoming dictionary

        Emulate a plug-in by providing access to attributes
        in the same way they are accessed using the remote object.
        This allows for it to be used by members of :mod:`pyblish.logic`.

        """

        process = None
        repair = None

        name = plugin["name"] + "Proxy"
        cls = type(name, (cls,), plugin)

        # Emulate function
        for name in ("process", "repair"):
            args = ", ".join(plugin["process"]["args"])
            func = "def {name}({args}): pass".format(name=name,
                                                     args=args)
            exec(func)

        cls.process = process
        cls.repair = repair

        cls.__orig__ = plugin

        return cls

    @classmethod
    def to_json(cls):
        return cls.__orig__.copy()
