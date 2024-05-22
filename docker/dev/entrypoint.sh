#!/bin/sh
python manage.py migrate --no-input
rm celerybeat.pid

exec "$@"