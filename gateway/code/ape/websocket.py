from json import loads
from logging import getLogger
from uuid import uuid4

from tornado.websocket import WebSocketHandler

from ape.browser import Browser
from ape.drivers.mq import BackendCommand

log = getLogger(__name__)


class BrowserHandler(WebSocketHandler):
    @property
    def _backend(self):
        return BackendCommand()

    def open(self):
        """
        Method is called when new websocket connection is established.
        """
        self.browser = Browser(self)
        log.info("{}: Browser connected".format(self.browser.id))
        self.browser.initialize()
        self.backend_initialize()

        log.info("{}: Sending handshake".format(self.browser.id))
        self.browser.send_handshake()

    def on_message(self, message):
        """
        Method is called when new data arrived from websocket (Browser)
        """
        message = loads(message)
        message["browser_id"] = self.browser.id
        self._backend.send_message(message)

    def on_close(self):
        """
        Method is called when Browser is disconnected.
        """
        log.info("{}: Browser disconnected".format(self.browser.id))
        self.browser.on_close()

    def check_origin(self, origin):
        """
        Override the origin check if needed
        """
        return True

    def backend_initialize(self):
        """
        Ensure that the backend queue is created.
        """
        self._backend.create_queue()
