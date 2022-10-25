#!/bin/bash -ex

cd "$(dirname "${BASH_SOURCE[0]}")"/.. || exit 1

apt-get update -yqq
apt-get install -yqq python3-pip

pip3 install pipenv
pipenv install --system --deploy --dev --ignore-pipfile
