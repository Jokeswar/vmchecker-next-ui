#!/bin/bash -ex

cd "$(dirname "${BASH_SOURCE[0]}")"/.. || exit 1

apt-get update -yqq
apt-get install -yqq python3-pip \
                     libldap2-dev libsasl2-dev # needed by python-ldap / django-auth-ldap

curl https://pyenv.run | bash

pip3 install pipenv
pipenv install --system --deploy --dev --ignore-pipfile
