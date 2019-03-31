class BrowserReactionHandler(object):
    typename = None

    def __init__(self, message, browser):
        self.message = message
        self.browser = browser

    @property
    def _queue(self):
        return self.browser._queue

    @property
    def _socket(self):
        return self.browser._socket

    def _is_proper_handler(self):
        return self.typename == self.message["type"]

    def react(self):
        raise NotImplemented()


