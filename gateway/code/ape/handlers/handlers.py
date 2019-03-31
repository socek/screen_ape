from copy import copy
from logging import getLogger


from ape.handlers.base import BrowserReactionHandler


log = getLogger(__name__)


class HandshakeHandler(BrowserReactionHandler):
    typename = "handshake"

    def react(self):
        if self.message["protocol_version"] != "1.0":
            self._socket.send(
                {
                    "type": "handshake",
                    "result": "fail",
                    "number": 1,
                    "message": "Unsupported protocol version",
                }
            )
        else:
            self.browser.initialize()
            log.info("B[{id}]: Handshake established".format(**self.browser.session))

    def _backend_initialize(self):
        """
        Ensure that the backend queue is created.
        """


class ActionHandler(BrowserReactionHandler):
    typename = "action"

    @property
    def _backend(self):
        return self.browser._backend

    def react(self):
        message = copy(self.message)
        message["browser_id"] = self.browser.session.id.hex
        self._backend.send_message(message)
        log.info("B[{id}]: Command forwarded".format(**self.browser.session))
