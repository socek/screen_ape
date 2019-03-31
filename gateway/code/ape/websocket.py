from logging import getLogger

from tornado.websocket import WebSocketHandler

from ape.browser import Browser


log = getLogger(__name__)


class WebsocketConnectionHandler(WebSocketHandler):
    def open(self):
        """
        Method is called when new websocket connection is established.
        """
        self.browser = Browser(self)

    def on_message(self, message):
        """
        Method is called when new data arrived from websocket (Browser)
        """
        self.browser.on_message(message)

    def on_close(self):
        """
        Method is called when Browser is disconnected.
        """
        self.browser.on_socket_disconnection()

    def check_origin(self, origin):
        """
        Override the origin check if needed
        """
        # TODO: What this method is for?
        return True
