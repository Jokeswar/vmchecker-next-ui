#!/bin/bash

cd "$(dirname "${BASH_SOURCE[0]}")"/.. || exit 1

sleep 2 # make sure that the DB container is up
./manage.py migrate
./manage.py populate_db
exec uwsgi --chdir="$(pwd)" \
    --env DJANGO_SETTINGS_MODULE=ui.settings \
    --processes 2 \
    --ini etc/ui.ini \
    --static-map /static="$(pwd)"/static
