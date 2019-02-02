import os
import sys
import logging

import structlog
from flask import g

CONFIGURED = False
USE_LOGGING = False

LOCAL_LOGGER = None


def _config_logger():
    global CONFIGURED
    global USE_LOGGING
    # this logging does not work with nose for whatever reason, so for unit tests we revert to using logger
    if os.environ.get('UNIT_TEST', '') == 'true':
        log_format = "%(asctime)s %(name)s@{}s [%(process)d] %(levelname)-8s %(message)s [in %(pathname)s:%(funcName)s:%(lineno)d]".format(
            os.getenv('HOSTNAME'))
        logging.basicConfig(stream=sys.stdout,
                            level=int(os.environ.get('FLASK_LOG_LEVEL', 10)),
                            format=log_format,
                            datefmt='%m-%d %H:%M')

        USE_LOGGING = True
    else:
        log_format = "%(message)s"
        logging.basicConfig(stream=sys.stdout,
                            level=int(os.environ.get('FLASK_LOG_LEVEL', 10)),
                            format=log_format,
                            datefmt='%m-%d %H:%M')

        processor_list = [
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder()
        ]
        if os.getenv('APP_ENV') == 'local':
            processor_list.append(structlog.dev.ConsoleRenderer(colors=False))
        else:
            processor_list.append(structlog.processors.JSONRenderer())

        structlog.configure(
            processors=processor_list,
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )

    CONFIGURED = True


def _set_logger(logger):
    if g:
        _set_logger_g(logger)
    else:
        _set_logger_local(logger)


def _set_logger_g(logger):
    g.logger = logger


def _set_logger_local(logger):
    global LOCAL_LOGGER

    LOCAL_LOGGER = logger


def _get_logger():
    if not CONFIGURED:
        _config_logger()

    if g:
        return _get_logger_g()
    else:
        return _get_logger_local()


def _get_logger_g():
    if not hasattr(g, 'logger'):
        _set_logger_g(structlog.get_logger('structlog.g'))
    return g.logger


def _get_logger_local():
    global LOCAL_LOGGER

    if not LOCAL_LOGGER:
        _set_logger_local(structlog.get_logger('structlog.local'))

    return LOCAL_LOGGER


def bind_all(*args, **kwargs):
    if USE_LOGGING:
        return
    _set_logger(_get_logger().bind(*args, **kwargs))


def debug(*args, **kwargs):
    if USE_LOGGING:
        message = "{} >>> {}".format(args[0], str(kwargs))
        return logging.debug(message)
    else:
        return _get_logger().debug(*args, **kwargs)


def info(*args, **kwargs):
    if USE_LOGGING:
        message = "{} >>> {}".format(args[0], str(kwargs))
        return logging.info(message)
    else:
        return _get_logger().info(*args, **kwargs)


def warning(*args, **kwargs):
    if USE_LOGGING:
        message = "{} >>> {}".format(args[0], str(kwargs))
        return logging.warning(message)
    else:
        return _get_logger().warning(*args, **kwargs)


def exception(*args, **kwargs):
    if USE_LOGGING:
        message = "{} >>> {}".format(args[0], str(kwargs))
        return logging.exception(message)
    else:
        return _get_logger().exception(*args, **kwargs)


def error(*args, **kwargs):
    if USE_LOGGING:
        message = "{} >>> {}".format(args[0], str(kwargs))
        return logging.error(message)
    else:
        return _get_logger().error(*args, **kwargs)


def critical(*args, **kwargs):
    if USE_LOGGING:
        message = "{} >>> {}".format(args[0], str(kwargs))
        return logging.critical(message)
    else:
        return _get_logger().critical(*args, **kwargs)
