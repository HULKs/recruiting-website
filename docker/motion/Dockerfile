FROM python:3
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY generate_animation.py ./
