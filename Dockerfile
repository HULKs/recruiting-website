FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt update
RUN apt install -y perl libmojolicious-perl libio-socket-ssl-perl \
                   libipc-run-perl libcapture-tiny-perl
RUN apt install -y python3 python3-opencv
COPY . /recruiting
WORKDIR /recruiting

ENV HULKS_RECRUITING_CONFIG=./recruiting.conf
CMD hypnotoad -f ./web
