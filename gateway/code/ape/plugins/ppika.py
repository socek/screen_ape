from logging import getLogger

from pika import ConnectionParameters
from pika import PlainCredentials
from pika.adapters.tornado_connection import TornadoConnection

log = getLogger(__name__)


class PikaClient(object):
    def __init__(self, app):
        self.app = app
        self.settings = self.app.settings
        self.channel = None

    def connect(self):
        log.info("Connecting to RabbitMQ...")
        user = self.settings["rabbit_user"]
        password = self.settings["rabbit_password"]

        parameters = dict(
            host=self.settings["rabbit_host"],
            port=self.settings["rabbit_port"],
            socket_timeout=self.settings["rabbit_connecion_timeout"],
        )

        try:
            credentials = PlainCredentials(user, password)
            param = ConnectionParameters(**parameters)

            self.connection = TornadoConnection(
                param, on_open_callback=self.on_connected
            )
        except Exception as e:
            log.error("Something went wrong with connection to RabbitMQ... %s", e)

    def on_connected(self, connection):
        """
        When we are completely connected to rabbitmq this is called
        """
        log.info("Succesfully connected to rabbitmq")
        self.channel = connection.channel()
        log.info("Awaiting for websocket connections...")


class PikaPlugin(object):
    def start(self, configurator):
        """
        This method will be called at the start of the Configurator. It will be
        called only once per process start. configurator is an object where all
        the configuratation is stored.
        """
        io_loop = configurator.io_loop
        timeout = configurator.settings["pika_io_loop_timeout"]

        self.pika = PikaClient(configurator)
        io_loop.add_timeout(timeout, self.pika.connect)

    def enter(self, context):
        """
        This method will be called when the Configurator will be used as context
        manager. This is the enter phase.
        """
        context.pika = self.pika
        context.rabbit = self.pika.channel

    def exit(self, *args, **kwargs):
        pass
