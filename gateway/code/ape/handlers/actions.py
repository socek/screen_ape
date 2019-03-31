from copy import copy
from logging import getLogger
from uuid import uuid4

from ape.handlers.base import BaseHandler
from ape.handlers.result import MessageToBackend
from ape.handlers.result import MessageToBrowser
from ape.handlers.types import GroupNames
from ape.handlers.types import TypeNames

log = getLogger(__name__)


class HandshakeHandler(BaseHandler):
    typename = TypeNames.handshake
    groupname = GroupNames.actions

    def _handle(self):
        if self.message["protocol_version"] != "1.0":
            message = {
                "type": "handshake",
                "result": "fail",
                "number": 1,
                "message": "Unsupported protocol version",
            }
            yield MessageToBrowser(message)

        else:
            self.browser.initialize()
            message = {
                "type": "handshake",
                "result": "ok",
                "browser_id": self.browser.session.id.hex,
            }
            yield MessageToBrowser(message)
            log.info("B[{id}]: Handshake established".format(**self.browser.session))


class ActionStatuses(object):
    sent = "sent"
    accepted = "accepted"
    not_accepted = "not accepted"


class ActionHandler(BaseHandler):
    typename = TypeNames.action
    groupname = GroupNames.actions

    def _handle(self):
        command_id = uuid4().hex
        message = copy(self.message)
        message["command_id"] = command_id
        yield MessageToBackend(message)
        yield MessageToBrowser(
            {
                "type": "action_status",
                "command_id": command_id,
                "status": ActionStatuses.sent,
            }
        )
        log.info("B[{id}]: Action forwarded".format(**self.browser.session))
