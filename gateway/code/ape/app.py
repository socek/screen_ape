from sapp.configurator import Configurator
from sapp.plugins import SettingsPlugin
from sapp.plugins.logging import LoggingPlugin


class ScreenApeConfigurator(Configurator):
    def append_plugins(self):
        self.add_plugin(SettingsPlugin("ape.settings"))
        self.add_plugin(LoggingPlugin())
