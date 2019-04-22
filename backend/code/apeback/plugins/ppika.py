from logging import getLogger

from pika import ConnectionParameters
from pika import PlainCredentials
from pika import BlockingConnection

log = getLogger(__name__)


class PikaClient(object):
    def __init__(self, app):
        self.app = app
        self.settings = self.app.settings
        self.channel = None

    def connect(self, consumer):
        log.info("Connecting to RabbitMQ...")
        user = self.settings["rabbit_user"]
        password = self.settings["rabbit_password"]
        queue = self.settings["backend_queue"]

        parameters = dict(
            host=self.settings["rabbit_host"],
            port=self.settings["rabbit_port"],
            socket_timeout=self.settings["rabbit_connecion_timeout"],
        )

        try:
            credentials = PlainCredentials(user, password)
            param = ConnectionParameters(**parameters)

            self.connection = BlockingConnection(param)
            self.channel = self.connection.channel()

            self.channel.basic_consume(
                queue=queue, auto_ack=True, on_message_callback=consumer
            )

        except Exception as e:
            log.error("Something went wrong with connection to RabbitMQ... %s", e)


class PikaPlugin(object):
    def start(self, configurator):
        """
        This method will be called at the start of the Configurator. It will be
        called only once per process start. configurator is an object where all
        the configuratation is stored.
        """
        self.client = PikaClient(configurator)

    def enter(self, context):
        """
        This method will be called when the Configurator will be used as context
        manager. This is the enter phase.
        """
        context.client = self.client
        context.rabbit = self.client.channel

    def exit(self, *args, **kwargs):
        pass
