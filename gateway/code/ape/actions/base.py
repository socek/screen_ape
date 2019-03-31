class BaseActionHandler(object):
    @property
    def _socket(self):
        return self.browser._socket

    def __init__(self, browser, message):
        self.browser = browser
        self.message = message

    def _validate(self, message):
        self.message = message
        return self._is_proper_handler

    def _action(self, message):
        pass

    def handle(self, body):
        message = loads(body)
        message = self._validate(message)
        action = self._action(message)
        self._socket.send(action)
