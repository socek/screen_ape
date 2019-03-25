from uuid import uuid4
from logging import getLogger

from tornado.websocket import WebSocketHandler

from ape.drivers.mq import backend
from ape.drivers.mq import queue
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
    def command(self):
        return WebsocketCommand(self)

    def open(self):
        self.screen = Screen()
        log.info("Screen connected: {}".format(self.screen._id))
        queue.create_queue_for_screen(self.screen)

        log.info("Sending handshake")
        self.command.send({"msg": "hello"})

    def on_message(self, message):
        pass

    def on_close(self):
        log.info("Screen disconnected")
        queue.destroy_queue(self.screen)

    def check_origin(self, origin):
        """
        Override the origin check if needed
        """
        return True
