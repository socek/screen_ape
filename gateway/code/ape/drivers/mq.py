from ape import app


class ScreenQueueCommand(object):
    """
    Commands responsible for managing messages to the screen.
    """

    _EXCHANGE = ""

    def create_queue_for_screen(self, screen):
        """
        Create queue for screen. This queue is for all messages that will be send to the screen.
        """
        with app("rabbit") as rabbit:
            rabbit.queue_declare(queue=screen.queue, exclusive=True)

    def destroy_queue(self, screen):
        """
        Destroy queue which was used for screen.
        """
        with app("rabbit") as rabbit:
            rabbit.queue_delete(queue=screen.queue)

    def send_message(self, screen, message):
        """
        Send message to the screen.
        """
        with app("rabbit") as rabbit:
            rabbit.basic_publish(
                exchange=self._EXCHANGE, routing_key=screen.queue, body=message
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
            rabbit.queue_declare(queue=self.queue)

    def send_message(self, message):
        with app("rabbit") as rabbit:
            rabbit.basic_publish(
                exchange=self._EXCHANGE, routing_key=self.queue, body=message
            )


queue = ScreenQueueCommand()
backend = BackendCommand()
