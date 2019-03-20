from pika import ConnectionParameters
from pika import PlainCredentials
from pika.adapters.tornado_connection import TornadoConnection


class PikaClient(object):
    def __init__(self, app):
        self.app = app
        self.channel = None

    def connect(self):
        print("Connecting to RabbitMQ...")
        host = self.app.settings["rabbit_host"]
        port = self.app.settings["rabbit_port"]
        user = self.app.settings["rabbit_user"]
        password = self.app.settings["rabbit_password"]

        try:
            credentials = PlainCredentials(user, password)
            param = ConnectionParameters(host=host, port=port, credentials=credentials)

            self.connection = TornadoConnection(
                param, on_open_callback=self.on_connected
            )
        except Exception as e:
            print("Something went wrong... %s", e)

    def on_connected(self, connection):
        """When we are completely connected to rabbitmq this is called"""
        print("Succesfully connected to rabbitmq")
        self.channel = connection.channel()


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
        print("\t\t <<< Enter Pika?")
        context.pika = self.pika
        context.rabbit = self.pika.channel

    def exit(self, *args, **kwargs):
        pass
