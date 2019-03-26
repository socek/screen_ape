from ape import app
from json import dumps


class BrowserQueueCommand(object):
    """
    Commands responsible for managing messages to the browser.
    """

    _EXCHANGE = ""

    def __init__(self, browser):
        self.browser = browser

    def create_queue(self):
        """
        Create queue for the Browser. This queue is for all messages that will be send to the browser.
        """
        queue = self.browser.queue_name
        with app("rabbit") as rabbit:
            rabbit.queue_declare(queue=queue, exclusive=True)
            rabbit.basic_consume(queue, self.browser.consumer)

    def destroy_queue(self):
        """
        Destroy queue which was used for the Browser.
        """
        with app("rabbit") as rabbit:
            rabbit.queue_delete(queue=self.browser.queue_name)

    def send_message(self, message):
        """
        Send message to the Browser.
        """
        with app("rabbit") as rabbit:
            rabbit.basic_publish(
                exchange=self._EXCHANGE, routing_key=self.browser.queue_name, body=message
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
