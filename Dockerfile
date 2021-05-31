from python:3.7-alpine
MAINTAINER Rishabh App dev ltd


ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirement.txt
RUN pip install -r /requirement.txt

RUN mkdir /app

WORKDIR /app

COPY ./app /app

RUN adduser -D user
USER user