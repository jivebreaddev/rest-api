#!/bin/sh
# creating a command as a set if one line fails all fails
set -e

python manage.py wait_for_db
python manage.py collectstatic --noinput
python manage.py migrate


uwsgi -socket :9000 --workers 4 --masters --enable-threads --module app.wsgi
