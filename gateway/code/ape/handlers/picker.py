from ape.handlers.base import BaseHandler
from ape.handlers.types import GroupNames


class HandlerPicker(object):
    module = None
    groupname = None

    def __init__(self, browser, message):
        self.message = message
        self.browser = browser

    def get_handlers(self):
        module = self._import()
        names = filter(lambda name: not name.startswith("_"), dir(module))
        for name in names:
            cls = getattr(module, name)
            is_handler = issubclass(cls, BaseHandler)
            is_in_proper_group = getattr(cls, "groupname", False) == self.groupname

            if is_handler and is_in_proper_group:
                yield cls

    def get_handler(self):
        for handler_cls in self.get_handlers():
            handler = handler_cls(self.browser, self.message)
            if handler._is_proper_handler():
                return handler

    def handle(self):
        return self.get_handler().handle()

    def _import(self):
        return __import__(self.module, globals(), locals(), [""])


class ActionHandlerPicker(HandlerPicker):
    module = "ape.handlers.actions"
    groupname = "actions"

class ReactionHandlerPicker(HandlerPicker):
    module = "ape.handlers.reactions"
    groupname = "reactions"
