from sapp.configurator import Configurator
from tornado.httpserver import HTTPServer
from tornado.log import enable_pretty_logging
from tornado.web import Application as Tornado


class TornadoPlugin(object):
    def start(self, configurator):
        enable_pretty_logging()
        configurator.tornado = Tornado(debug=True, serve_traceback=True)
        configurator._http_server = HTTPServer(configurator.tornado)

    def enter(self, context):
        pass

    def exit(self, *args, **kwargs):
        pass
