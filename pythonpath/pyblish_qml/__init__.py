from .version import version, version_info


class _Settings(object):

    def __init__(self):
        self.ContextLabel = "Context"
        self.WindowTitle = "Pyblish"
        self.WindowSize = (430, 600)
        self.WindowPosition = (100, 100)
        self.HeartbeatInterval = 60

        self._callbacks = dict()
        self._current_port = 0
        self._port_changed_callbacks = list()

        self.__initialised = True

    def __str__(self):
        return str(self.to_dict())

    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        return dict((k, getattr(self, k)) for k in self.__dict__
                    if not k.startswith("_"))

    def from_dict(self, settings):
        self.__dict__.update(settings)

    def current_port(self):
        """Return port through which QML is currently communicating"""
        return self._current_port

    def set_current_port(self, port):
        """Set the port with which to communicate"""
        self._current_port = port
        for func in self._port_changed_callbacks:
            func(port)

    def register_port_changed_callback(self, func):
        """When the current port changes, trigger the supplied callable

        Arguments:
            func (callable): Callable to run upon a new client registering
                interest in displaying the GUI.
        """

        self._port_changed_callbacks.append(func)


settings = _Settings()
