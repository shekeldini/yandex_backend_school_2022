FROM python:3.10.5-slim-buster

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

RUN apt update && \
   apt install --no-install-recommends --no-install-suggests --assume-yes \
    # For Psycopg
    gcc \
    python3-dev \
    libpq-dev \
    libmagic1

RUN python -m pip install --upgrade pip

ENV app app
RUN mkdir /$app
COPY ./src/requirements.txt /$app

WORKDIR /$app

RUN pip install -r requirements.txt
