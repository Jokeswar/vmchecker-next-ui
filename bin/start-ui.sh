#!/bin/bash

cd "$(dirname "${BASH_SOURCE[0]}")"/.. || exit 1

sleep 2 # make sure that the DB container is up
./manage.py migrate
./manage.py runserver 0.0.0.0:7000
