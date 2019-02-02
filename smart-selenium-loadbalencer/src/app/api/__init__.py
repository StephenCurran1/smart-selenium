"""init file for communication service"""
import os
import datadog
from . import version1
from flask import Flask  # pragma: no cover
from ..lib import logger

from . import version1

datadog_options = {
    'statsd_host': os.environ.get('STATSD_HOST', 'statsd.monitoring'),
    'statsd_port': os.environ.get('STATSD_PORT', '8125')
}

datadog.initialize(**datadog_options)
logger.debug("statsd initialized")

smart_selenium = Flask(__name__)
smart_selenium.register_blueprint(version1.send, url_prefix='/wd')
logger.info("smart_selenium started")

from . import routes

