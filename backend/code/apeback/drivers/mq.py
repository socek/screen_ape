from json import dumps

from apeback import app


class BrowserQueueCommand(object):
    """
    Commands responsible for managing messages to the browser.
    """

    _EXCHANGE = ""

    def __init__(self, browser_uuid):
        self.browser_uuid = browser_uuid

    def send_message(self, message):
        """
        Send message to the Browser.
        """
        with app("rabbit") as rabbit:
            rabbit.basic_publish(
                exchange=self._EXCHANGE, routing_key=self.browser_uuid, body=dumps(message)
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
                exchange=self._EXCHANGE, routing_key=self.queue, body=dumps(message)
            )

    def engage_consumer(self, callback):
        with app("rabbit") as rabbit:
            rabbit.basic_consume(
                queue=self.queue, auto_ack=True, on_message_callback=callback
            )
