FROM python:3.7.5-slim

WORKDIR /web-back

COPY requirements.txt .

RUN apt-get update
RUN apt-get install -y locales locales-all
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

RUN pip install -r requirements.txt

COPY . .