FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /online_store

COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY . /online_store
