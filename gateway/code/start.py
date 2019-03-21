from ape import app
from ape.websocket import ScreenHandler
from ape.drivers.mq import backend


def start():
    app.start("default")
    app.tornado.add_handlers(".*", [(r"/", ScreenHandler, {})])
    backend.create_queue()
    app.run_io_loop()


if __name__ == "__main__":
    start()
