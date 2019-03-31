class BaseAction(object):
    @property
    def _socket(self):
        return self.browser._socket

    def __init__(self, browser):
        self.browser = browser

    def handle(self, body):
        data = loads(body)
        self._socket.send({"type": "command", "body": data})
