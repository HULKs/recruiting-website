FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install --no-install-recommends -y \
    iproute2 inotify-tools \
    && rm -Rf /var/lib/apt/lists/*

CMD tail -f /dev/null
