FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    perl libmojolicious-perl libio-socket-ssl-perl libipc-run-perl \
    libcapture-tiny-perl libjson-xs-perl python3 python3-opencv \
    && rm -rf /var/lib/apt/lists/*

COPY . /recruiting
WORKDIR /recruiting

ENV HULKS_RECRUITING_CONFIG=./recruiting.conf
CMD hypnotoad -f ./web
