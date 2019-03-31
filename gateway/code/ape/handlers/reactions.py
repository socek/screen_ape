from logging import getLogger

from ape.handlers.base import BaseHandler
from ape.handlers.result import MessageToBrowser
from ape.handlers.types import GroupNames
from ape.handlers.types import TypeNames

log = getLogger(__name__)


class ReactionHandler(BaseHandler):
    typename = TypeNames.reaction
    groupname = GroupNames.reactions

    def _handle(self):
        yield MessageToBrowser(message)
        log.info("B[{id}]: Reaction forwarded".format(**self.browser.session))


class RedirectHandler(BaseHandler):
    typename = TypeNames.redirect
    groupname = GroupNames.reactions

    def _handle(self):
        yield MessageToBrowser(message)
        log.info(
            "B[{0}]: Redirect to {1}".format(self.browser.session.id, message["path"])
        )
