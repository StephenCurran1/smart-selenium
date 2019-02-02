#!/usr/bin/env python
import logging
from app.api import smart_selenium



def run_test_app():
    smart_selenium.run(host='0.0.0.0', debug=True)


if __name__ == "__main__":
    logging.debug("about to start smart selenium load balencer flask-app")
    run_test_app()
