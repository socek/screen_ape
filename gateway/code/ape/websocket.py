from logging import getLogger
from uuid import uuid4

from tornado.websocket import WebSocketHandler

from ape.drivers.mq import BackendCommand
from ape.drivers.mq import ScreenQueueCommand
from ape.drivers.ws import WebsocketCommand

log = getLogger(__name__)


class Screen(object):
    @property
    def queue(self):
        return self._id.hex

    def __init__(self):
        self._id = uuid4()


class ScreenHandler(WebSocketHandler):
    @property
    def _screen(self):
        return WebsocketCommand(self)

    @property
    def _backend(self):
        return BackendCommand()

    @property
    def _screen_queue(self):
        return ScreenQueueCommand(self.screen)


    def open(self):
        self.screen = Screen()
        log.info("Screen connected: {}".format(self.screen._id))
        self._screen_queue.create_queue()
        self._backend.create_queue()

        log.info("Sending handshake")
        self._screen.send({"msg": "hello"})
        self._backend.send_message({"msg": "hello"})

    def on_message(self, message):
        pass

    def on_close(self):
        log.info("Screen disconnected")
        self._screen_queue.destroy_queue(self.screen)

    def check_origin(self, origin):
        """
        Override the origin check if needed
        """
        return True
