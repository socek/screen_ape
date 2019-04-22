from logging import INFO
from logging import getLogger

from decouple import config
from sapp.plugins.settings import PrefixedStringsDict


def default():
    settings = {"paths": PrefixedStringsDict("/code/")}
    logging(settings)
    rabbit(settings)
    return settings


def logging(settings):
    formatter = config("LOGGING_FORMATTER", "descriptive")
    settings["logging"] = {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "generic": {"format": "%(message)s"},
            "descriptive": {
                "format": "%(asctime)s %(levelname)-5.5s [%(name)s][%(threadName)s] %(message)s"
            },
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": formatter,
            }
        },
        "loggers": {
            "": {"level": "DEBUG", "handlers": ["console"]},
            "apeback": {"level": "DEBUG", "handlers": []},
            "pika": {"level": "CRITICAL", "handlers": []},
        },
    }


def rabbit(settings):
    settings["rabbit_host"] = config("RABBIT_HOST")
    settings["rabbit_port"] = config("RABBIT_PORT", 5672, int)
    settings["rabbit_user"] = config("RABBIT_USER", "guest")
    settings["rabbit_password"] = config("RABBIT_PASSWORD", "guest")
    settings["rabbit_connecion_timeout"] = config("RABBIT_SOCKET_TIMEOUT", 2, float)

    settings["backend_queue"] = config("BACKEND_QUEUE", "backend")
