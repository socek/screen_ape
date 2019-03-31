from copy import copy


class Message(object):
    def __init__(self, message):
        self.message = message

    def initalize(self, browser):
        self.browser = browser

    def send(self):
        raise NotImplemented()


class MessageToBrowser(Message):
    @property
    def _socket(self):
        return self.browser._socket

    def send(self):
        self._socket.send(self.message)


class MessageToBackend(Message):
    @property
    def _backend(self):
        return self.browser._backend

    def send(self):
        message = copy(self.message)
        message["browser_id"] = self.browser.session.id.hex
        self._backend.send_message(message)
