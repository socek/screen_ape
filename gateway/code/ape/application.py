from sapp.configurator import Configurator
from sapp.plugins import SettingsPlugin
from sapp.plugins.logging import LoggingPlugin
from tornado.ioloop import IOLoop

from ape.plugins.ppika import PikaPlugin
from ape.plugins.ptornado import TornadoPlugin


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


class ScreenApeConfigurator(Configurator):
    def __init__(self):
        super().__init__()
        self.io_loop = IOLoop.instance()

    def append_plugins(self):
        self.add_plugin(SettingsPlugin("ape.settings"))
        self.add_plugin(TornadoPlugin())
        self.add_plugin(PikaPlugin())
        self.add_plugin(LoggingPlugin())

    def run_io_loop(self):
        self._http_server.listen(self.settings["tornado_port"])
        try:
            print("Starting application...")
            self.io_loop.start()
        except KeyboardInterrupt:
            self.io_loop.stop()

    def __enter__(self):
        return self.create_context()

    def __call__(self, *args):
        return FragmentContext(self, args)
