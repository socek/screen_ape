from logging import getLogger


log = getLogger(__name__)


class BaseHandler(object):
    typename = None
    groupname = None

    def __init__(self, browser, message):
        self.message = message
        self.browser = browser

    @property
    def _queue(self):
        return self.browser._queue

    @property
    def _socket(self):
        return self.browser._socket

    @property
    def _backend(self):
        return self.browser._backend

    def _is_proper_handler(self):
        return self.typename == self.message["type"]

    def _handle(self):
        pass

    def handle(self):
        for result in self._handle():
            result.initalize(self.browser)
            result.send()
