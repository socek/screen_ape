from logging import getLogger
from uuid import uuid4
from json import loads

from tornado.websocket import WebSocketHandler

from ape.drivers.mq import BackendCommand
from ape.drivers.mq import ScreenQueueCommand
from ape.drivers.ws import WebsocketCommand

log = getLogger(__name__)


class Screen(object):
    @property
    def _queue(self):
        return ScreenQueueCommand(self)

    @property
    def _screen(self):
        return WebsocketCommand(self.handler)

    @property
    def queue(self):
        return self.id

    @property
    def id(self):
        return self._id.hex

    def __init__(self, handler):
        self._id = uuid4()
        self.handler = handler

    def initialize(self):
        self._queue.create_queue()

    def send_handshake(self):
        self._screen.send({
            "type": "handshake",
            "body": {
                "screen_id": self.id,
            }})

    def consumer(self, channel, method, properties, body):
        data = loads(body)
        self._screen.send({
            "type": "command",
            "body": data})


class ScreenHandler(WebSocketHandler):
    @property
    def _backend(self):
        return BackendCommand()

    def open(self):
        self.screen = Screen(self)
        log.info("Screen connected: {}".format(self.screen._id))
        self.screen.initialize()
        self.backend_initialize()

        log.info("Sending handshake")
        self.screen.send_handshake()

    def on_message(self, message):
        message = loads(message)
        message["screen_id"] = self.screen.id
        self._backend.send_message(message)

    def on_close(self):
        log.info("Screen disconnected")
        self._screen_queue.destroy_queue()

    def check_origin(self, origin):
        """
        Override the origin check if needed
        """
        return True

    def backend_initialize(self):
        self._backend.create_queue()
