FROM selenium/hub 

USER root

RUN apt update && apt install  -y \
    python3.6 \
    python3-pip \
    supervisor \
    zip \
    mysql-client \
    python3-dev \
    curl \
    libffi-dev \
    make \
    gcc \
    g++ \
    musl-dev && \
    pip3 install --upgrade pip uwsgi Flask setuptools cython nose coverage ujson requests elasticsearch python-rapidjson \
    datadog hiredis structlog && \
    mkdir -p /srv/root && \
    mkdir -p /var/log/supervisor && \
    mkdir -p /srv/root 

# As integer, maps to "maxSession"
ENV GRID_MAX_SESSION 0
# In milliseconds, maps to "newSessionWaitTimeout"
ENV GRID_NEW_SESSION_WAIT_TIMEOUT -1
# As a boolean, maps to "throwOnCapabilityNotPresent"
ENV GRID_THROW_ON_CAPABILITY_NOT_PRESENT true
# As an integer
ENV GRID_JETTY_MAX_THREADS -1
# In milliseconds, maps to "cleanUpCycle"
ENV GRID_CLEAN_UP_CYCLE 5000
# In seconds, maps to "browserTimeout"
ENV GRID_BROWSER_TIMEOUT 0
# In seconds, maps to "timeout"
ENV GRID_TIMEOUT 1800
# Debug
ENV GRID_DEBUG false
# As integer, maps to "port"
ENV GRID_HUB_PORT 4444
# As string, maps to "host"
ENV GRID_HUB_HOST "0.0.0.0"

ADD conf/supervisord.conf /etc/supervisord.confs

ENV NUM_OF_PROCESSES=1
# # Add Scripts
ADD scripts/start.sh /start.sh
RUN chmod 755 /start.sh

# # Add ini
ADD conf/uwsgi-service.ini /uwsgi-service.ini

# # copy in code
ADD smart-selenium-hub/src/ /srv/root/


EXPOSE 80

CMD ["/start.sh"]

EXPOSE 4444
