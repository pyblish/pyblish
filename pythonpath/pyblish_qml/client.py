import httplib
import xmlrpclib


class TimeoutTransport(xmlrpclib.Transport):
    """Requests should happen instantly"""
    def __init__(self, timeout=5, *args, **kwargs):
        xmlrpclib.Transport.__init__(self, *args, **kwargs)
        self.timeout = timeout

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


def proxy(timeout=5):
    """Return proxy at default location of Pyblish QML"""
    return xmlrpclib.ServerProxy(
        "http://127.0.0.1:9090",
        transport=TimeoutTransport(timeout),
        allow_none=True)
