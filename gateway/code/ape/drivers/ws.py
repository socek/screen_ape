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

    def _send(self, data):
        self._write(dumps(data))

    def handshake(self, _id):
        log.info("{}: Sending handshake".format(_id))
        self._send({"type": "handshake", "result": "ok", "screen_id": _id})

    def consume_command(self, message):
        self._send({"type": "command", "body": message})
