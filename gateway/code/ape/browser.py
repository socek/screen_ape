from logging import getLogger
from uuid import uuid4

from ape.drivers.mq import BrowserQueueCommand
from ape.drivers.ws import WebsocketCommand

log = getLogger(__name__)


class Browser(object):
    @property
    def _queue(self):
        return BrowserQueueCommand(self)

    @property
    def _browser(self):
        return WebsocketCommand(self.handler)

    @property
    def queue_name(self):
        return self.id

    @property
    def id(self):
        return self._id.hex

    def __init__(self, handler):
        self._id = uuid4()
        self.handler = handler

    def initialize(self):
        """
        Create queue for receiving data for this Browser.
        """
        self._queue.create_queue()

    def send_handshake(self):
        """
        Send handshake after connection with Browser is established.
        """
        self._browser.send({"type": "handshake", "result": "ok", "screen_id": self.id})

    def consumer(self, channel, method, properties, body):
        """
        React on new data received from the Browser queue.
        """
        data = loads(body)
        self._browser.send({"type": "command", "body": data})

    def on_close(self):
        """
        React on closing the connection to the Browser.
        """
        self._queue.destroy_queue()
