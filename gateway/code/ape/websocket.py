from uuid import uuid4

from tornado.websocket import WebSocketHandler

from ape import app


class Screen(object):
    @property
    def queue(self):
        return self._id.hex

    def __init__(self):
        self._id = uuid4()

    def create_queue(self):
        with app('rabbit') as rabbit:
            rabbit.queue_declare(queue=self.queue, exclusive=True)
            self.publish()

    def destroy_queue(self):
        with app('rabbit') as rabbit:
            rabbit.queue_delete(queue=self.queue)

    def publish(self):
        with app('rabbit') as rabbit:
            rabbit.basic_publish(exchange="", routing_key=self.queue, body="Hello World!")


class ScreenHandler(WebSocketHandler):
    def open(self):
        self.screen = Screen()
        print("Screen connected: {}".format(self.screen._id))
        self.screen.create_queue()

        print("Sending hello")
        self.write_message(u"Hellow")

    def on_message(self, message):
        self.write_message(u"You said: " + message)

    def on_close(self):
        print("WebSocket closed")
        self.screen.destroy_queue()

    def check_origin(self, origin):
        """
        Override the origin check if needed
        """
        return True
