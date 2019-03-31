from ape.actions.base import BaseActionHandler


class CommandAction(BaseActionHandler):
    typename = "action"

    def _is_proper_handler(self, message):
        return self.typename == self.message["type"]

    def _action(self, message):
        pass
