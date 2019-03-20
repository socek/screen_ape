from decouple import config
from sapp.plugins.settings import PrefixedStringsDict


def default():
    settings = {"paths": PrefixedStringsDict("/code/")}
    websockets(settings)
    logging(settings)
    return settings


def logging(settings):
    settings["logging"] = {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "generic": {
                "format": "%(asctime)s %(levelname)-5.5s [%(name)s][%(threadName)s] %(message)s"
            }
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "generic",
            }
        },
        "loggers": {
            "root": {"level": "DEBUG", "handlers": ["console"]},
            "wstask": {"level": "DEBUG", "handlers": ["console"], "qualname": "wstask"},
            "celery": {"handlers": ["console"], "level": "ERROR"},
        },
    }


def websockets(settings):
    settings["websocket_port"] = 18765
