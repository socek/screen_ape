from ape import app
from json import dumps


class ScreenQueueCommand(object):
    """
    Commands responsible for managing messages to the screen.
    """

    _EXCHANGE = ""

    def __init__(self, screen):
        self.screen = screen

    def create_queue(self):
        """
        Create queue for screen. This queue is for all messages that will be send to the screen.
        """
        queue = self.screen.queue
        with app("rabbit") as rabbit:
            rabbit.queue_declare(queue=queue, exclusive=True)
            rabbit.basic_consume(queue, self.screen.consumer)

    def destroy_queue(self):
        """
        Destroy queue which was used for screen.
        """
        with app("rabbit") as rabbit:
            rabbit.queue_delete(queue=self.screen.queue)

    def send_message(self, message):
        """
        Send message to the screen.
        """
        with app("rabbit") as rabbit:
            rabbit.basic_publish(
                exchange=self._EXCHANGE, routing_key=self.screen.queue, body=message
            )


class BackendCommand(object):
    """
    Commands responsible for sending messages to the backend.
    """

    _EXCHANGE = ""

    @property
    def queue(self):
        with app("settings") as settings:
            return settings["backend_queue"]

    def create_queue(self):
        with app("rabbit") as rabbit:
            rabbit.queue_declare(queue="backend")

    def send_message(self, message):
        with app("rabbit") as rabbit:
            rabbit.basic_publish(
                exchange=self._EXCHANGE, routing_key=self.queue, body=dumps(message)
            )
