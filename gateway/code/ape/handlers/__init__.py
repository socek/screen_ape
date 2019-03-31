from ape.handlers.base import BrowserReactionHandler
import ape.handlers.handlers as handlers


class HandlerPicker(object):
    def __init__(self, browser, message):
        self.message = message
        self.browser = browser


    def get_all_handlers(self):
        names = list(filter(lambda name: not name.startswith("_"), dir(handlers)))
        classes = [getattr(handlers, name) for name in names]

        for cls in classes:
            is_handler_child = issubclass(cls, BrowserReactionHandler)
            is_handler_parent = cls == BrowserReactionHandler
            if (is_handler_child and not is_handler_parent):
                yield cls

    def get_handler(self):
        for handler_cls in self.get_all_handlers():
            handler = handler_cls(self.message, self.browser)
            if handler._is_proper_handler():
                return handler

    def react(self):
        return self.get_handler().react()
