FROM python:3.8.10-buster

WORKDIR /opt/ui

ADD ui ./ui
ADD bin ./bin
ADD etc ./etc
COPY Pipfile.lock ./
COPY Pipfile ./
COPY manage.py ./

RUN set -e \
    && ./bin/provision-system.sh

RUN ./manage.py collectstatic --no-input

EXPOSE 7000

CMD ./bin/start-ui.sh
