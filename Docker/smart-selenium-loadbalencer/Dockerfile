FROM python:3.6-alpine

RUN apk --update add bash \
    supervisor \
    zip \
    mysql-client \
    openssl \
    openssh \
    python3-dev \
    curl \
    curl-dev \
    libffi-dev \
    make \
    gcc \
    g++ \
    linux-headers \
    musl-dev \
    pcre-dev && \ 
    pip3 install --upgrade pip uwsgi Flask setuptools cython nose coverage ujson requests elasticsearch python-rapidjson \
    datadog hiredis structlog && \
    rm -r /root/.cache && \
    mkdir -p /srv/root && \
    mkdir -p /var/log/supervisor && \
    mkdir -p /srv/root

ADD conf/supervisord.conf /etc/supervisord.conf

# # Add Scripts
ADD scripts/start.sh /start.sh
RUN chmod 755 /start.sh

# # Add ini
ADD conf/uwsgi-service.ini /uwsgi-service.ini

# # copy in code
ADD smart-selenium-loadbalencer/src/ /srv/root/


EXPOSE 80

CMD ["/start.sh"]
