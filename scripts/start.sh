#!/bin/bash

# usgwi mods
if [ -z "$NUM_OF_PROCESSES" ]; then
  echo "Please set NUM_OF_PROCESSES"
  exit 1
else
  sed -i "s#NUM_OF_PROCESSES#$NUM_OF_PROCESSES#g" /uwsgi-service.ini
fi
i

# unit test html output
if [[ "$APP_ENV" == "local" ]] ; then
    L1='static-index    = index.html'
    L2='static-map      = /tests=/srv/root/tests/htmlcov'
    L3='route           = /app_(.*)\\.html static:/srv/root/tests/htmlcov/app_$1.html'
    L4='route           = /(.*)\\.js static:/srv/root/tests/htmlcov/$1.js'
    L5='route           = /style.css static:/srv/root/tests/htmlcov/style.css'
    L6='route           = /keybd_closed.png static:/srv/root/tests/htmlcov/keybd_closed.png'
    L7='route           = /keybd_open.png static:/srv/root/tests/htmlcov/keybd_open.png'
    sed -i "s#\#UNIT_TEST#$L1\n$L2\n$L3\n$L4\n$L5\n$L6\n$L7#" /uwsgi-service.ini
fi

# Start supervisord and services
exec /usr/bin/supervisord -n -c /etc/supervisord.conf

