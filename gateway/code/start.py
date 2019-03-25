from ape import app
from ape.websocket import ScreenHandler
from ape.drivers.mq import backend

from logging import getLogger



def start():
    app.start("default")
    app.tornado.add_handlers(".*", [(r"/", ScreenHandler, {})])
    app.run_io_loop()


if __name__ == "__main__":
    start()
