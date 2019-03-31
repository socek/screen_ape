from json import dumps
from logging import getLogger


log = getLogger(__name__)


class WebsocketCommand(object):
    """
    This class is responsible for sending the messages to the screen using websocket.
    """

    def __init__(self, handler):
        self.handler = handler

    def _write(self, *args, **kwargs):
        return self.handler.write_message(*args, **kwargs)

    def send(self, data):
        self._write(dumps(data))

