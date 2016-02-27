"""The Pyblish RPC Server

Attributes:
    current_server_thread: A reference to the currently running
        server, if started using start_async_production_server.

"""


import sys
# import base64
import threading
import SocketServer
from SimpleXMLRPCServer import (
    SimpleXMLRPCServer,
    SimpleXMLRPCRequestHandler
)

import pyblish.api
import pyblish.lib
import pyblish.logic

import pyblish_rpc
import service as service_

self = sys.modules[__name__]
self.current_server_thread = None
self.current_server = None


def default_wrapper(func, *args, **kwargs):
    return func(*args, **kwargs)


class RpcServer(SocketServer.ThreadingMixIn, SimpleXMLRPCServer):
    """The Pyblish RPC Server

    Support multiple requests simultaneously. This is important,
    as we will still want to emit heartbeats during a potentially
    long process.

    About paths, the API is accessible from both the root /pyblish and
    suffixed with an exact version, such as /pyblish/v1. The root always
    references the latest version.

    """

    def __init__(self, path, *args, **kwargs):
        class VerifyingRequestHandler(SimpleXMLRPCRequestHandler):
            rpc_paths = ("/pyblish", path)

            def parse_request(this):
                if SimpleXMLRPCRequestHandler.parse_request(this):
                    if self.authenticate(this.headers):
                        return True
                else:
                    this.send_error(401, "Authentication failed")

                return False

        SimpleXMLRPCServer.__init__(
            self,
            requestHandler=VerifyingRequestHandler,
            *args,
            **kwargs)

    def authenticate(self, headers):
        """TODO(marcus): Implement basic authentication"""
        # basic, _, encoded = headers.get("Authorization").partition(" ")
        # assert basic == "Basic", "Only basic authentication supported"
        # username, _, password = base64.b64decode(encoded).partition(":")
        # assert username == "marcus"
        # assert password == "pass"
        return True

    def _dispatch(self, *args):
        wrapper = pyblish_rpc.dispatch_wrapper() or default_wrapper
        return wrapper(SimpleXMLRPCServer._dispatch,
                       self, *args)


def kill():
    """Shutdown a running server"""
    print "Shutting down.."
    return self.current_server.shutdown()


def _server(port, service):
    server = RpcServer(
        "/pyblish",
        ("127.0.0.1", port),
        allow_none=True,
        logRequests=False)

    server.register_function(kill)
    server.register_introspection_functions()
    server.register_instance(service, allow_dotted_names=True)

    self.current_server = server

    return server


def _serve(port, service=None):
    if service is None:
        service = service_.RpcService()

    server = _server(port, service)
    print("Listening on %s:%s" % server.server_address)
    server.serve_forever()


def start_production_server(port, service=None):
    """Run server with optimisations

    Arguments:
        port (int): Port at which to listen for incoming requests
        service (RpcService): Service responding to requests

    """

    return _serve(port, service)


def start_async_production_server(port, service=None):
    """Start a threaded version of production server

    Returns Thread object.

    """

    def worker():
        start_production_server(port, service)

    thread = threading.Thread(target=worker)
    thread.daemon = True
    thread.start()

    self.current_server_thread = thread

    return thread


def start_debug_server(port=6000, delay=0.5):
    """Start debug server

    This server uses a mocked up service to fake the actual
    behaviour and data of a generic host; incuding faked time
    it takes to perform a task.

    Arguments:
        port (int, optional): Port at which to listen for requests.
            Defaults to 6000.
        delay (float, optional): Simulate time taken to process requests.
            Defaults to 0.5 seconds.

    """

    pyblish.lib.setup_log("pyblish")
    service = service_.MockRpcService()
    return _serve(port, service)
