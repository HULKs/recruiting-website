FROM python:3
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ball.png body.png foot.png ground.png thigh.png tibia.png JetBrainsMono-Regular.ttf ./
COPY *.py ./
