FROM python:3.8.10-buster

WORKDIR /opt/api

ADD api ./api
ADD bin ./bin
COPY Pipfile.lock ./
COPY manage.py ./

RUN set -e \
    && ./bin/provision-system.sh

RUN ./manage.py collectstatic --no-input

EXPOSE 8000
CMD ./bin/startapi.sh
