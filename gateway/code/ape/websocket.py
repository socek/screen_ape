from uuid import uuid4

from tornado.websocket import WebSocketHandler

from ape.drivers.mq import backend
from ape.drivers.mq import queue
from ape.drivers.ws import WebsocketCommand


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
        print("Screen connected: {}".format(self.screen._id))
        queue.create_queue_for_screen(self.screen)

        print("Sending hello")
        self.command.send({"msg": "hello"})

    def on_message(self, message):
        pass

    def on_close(self):
        print("WebSocket closed")
        queue.destroy_queue(self.screen)

    def check_origin(self, origin):
        """
        Override the origin check if needed
        """
        return True
