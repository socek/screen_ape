from decouple import config
from sapp.plugins.settings import PrefixedStringsDict


def default():
    settings = {"paths": PrefixedStringsDict("/code/")}
    logging(settings)
    tornado(settings)
    rabbit(settings)
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
            "ape": {"level": "DEBUG", "handlers": ["console"]},
            "tornado": {"level": "DEBUG", "handlers": ["console"]},
        },
    }


def tornado(settings):
    settings["debug"] = config("DEBUG", False, bool)
    settings["tornado_port"] = config("TORNADO_PORT", 18765)


def rabbit(settings):
    settings["rabbit_host"] = config("RABBIT_HOST")
    settings["rabbit_port"] = config("RABBIT_PORT", 5672, int)
    settings["rabbit_user"] = config("RABBIT_USER", "guest")
    settings["rabbit_password"] = config("RABBIT_PASSWORD", "guest")
    settings["pika_io_loop_timeout"] = config("PIKA_IO_LOOP_TIMEOUT", 500, int)

    settings["backend_queue"] = config("BACKEND_QUEUE", "backend")
