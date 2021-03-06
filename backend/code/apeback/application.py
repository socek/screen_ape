from logging import getLogger

from sapp.configurator import Configurator
from sapp.plugins import SettingsPlugin
from sapp.plugins.logging import LoggingPlugin

from apeback.plugins.ppika import PikaPlugin


log = getLogger(__name__)


class FragmentContext(object):
    def __init__(self, configurator, args):
        self.configurator = configurator
        self.args = args

    def __enter__(self):
        ctx = self.configurator.__enter__()
        if len(self.args) == 0:
            return None
        elif len(self.args) == 1:
            return getattr(ctx, self.args[0])
        else:
            return [getattr(ctx, arg) for arg in self.args]

    def __exit__(self, *args, **kwargs):
        ctx = self.configurator.__exit__(*args, **kwargs)


class ScreenApeBackendConfigurator(Configurator):
    def add_plugin(self, plugin):
        super().add_plugin(plugin)
        return plugin

    def append_plugins(self):
        self.add_plugin(SettingsPlugin("apeback.settings"))
        self.pika = self.add_plugin(PikaPlugin())
        self.add_plugin(LoggingPlugin())

    def __enter__(self):
        return self.create_context()

    def __call__(self, *args):
        return FragmentContext(self, args)

    def start_consumer(self, consumer):
        self.start("default")
        client = self.pika.client
        client.connect(consumer)
        print("Started consuming...")
        client.channel.start_consuming()
