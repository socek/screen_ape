from ape import app
from ape.websocket import BrowserHandler

from logging import getLogger



def start():
    app.start("default")
    app.tornado.add_handlers(".*", [(r"/", BrowserHandler, {})])
    app.run_io_loop()


if __name__ == "__main__":
    start()
