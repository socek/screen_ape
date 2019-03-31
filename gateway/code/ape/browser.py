from json import loads
from logging import getLogger
from uuid import uuid4

from ape.drivers.mq import BackendCommand
from ape.drivers.mq import BrowserQueueCommand
from ape.drivers.ws import WebsocketCommand
from ape.handlers import ActionHandlerPicker

log = getLogger(__name__)


class SessionVars(dict):
    def __init__(self):
        self.id = uuid4()
        self.logged_in = False

    def __getattr__(self, attr):
        return self[attr]

    def __setattr__(self, attr, value):
        self[attr] = value


class Browser(object):
    @property
    def _queue(self):
        return BrowserQueueCommand(self)

    @property
    def _socket(self):
        return WebsocketCommand(self.connection)

    @property
    def _backend(self):
        return BackendCommand()

    def __init__(self, connection):
        self.connection = connection
        self.session = SessionVars()
        log.info("B[{id}]: Browser connected".format(**self.session))

    def initialize(self):
        """
        Create queue for receiving data for this Browser.
        """
        self._queue.create_queue()
        self._backend.create_queue()
        log.info("B[{id}]: Queues created".format(**self.session))

    def consumer(self, channel, method, properties, body):
        """
        React on new data received from the Browser queue.
        """
        data = loads(body)
        self._socket.send({"type": "command", "body": data})

    def on_socket_disconnection(self):
        """
        Method is called when Browser is disconnected.
        """
        self._queue.destroy_queue()
        log.info("B[{id}]: Browser disconnected".format(**self.session))

    def on_message(self, message):
        """
        Method is called when new data arrived from websocket (Browser)
        """
        ActionHandlerPicker(self, loads(message)).handle()
