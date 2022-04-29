FROM python:3.8-slim-buster

ARG REPO_USER=read-user
ARG REPO_PWD

RUN apt-get update && \
    apt-get install -y vim git pkg-config cmake g++ wget unzip libjpeg62-turbo ffmpeg libavcodec-dev \
    libavformat-dev libavutil-dev libswscale-dev libavresample-dev ninja-build


RUN pip install --upgrade pip

WORKDIR /code
ADD . .

