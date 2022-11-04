FROM python:3.10

ENV POETRY_VERSION 1.1.13

WORKDIR /app

RUN pip install virtualenv

COPY . /app

RUN virtualenv -p python3 venv && . venv/bin/activate && pip install -r requirements.txt
