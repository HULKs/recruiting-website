FROM pandoc/core:2.9.1.1 AS pandoc

################################################################################
FROM alpine:3.11 AS recruiting-website-static-builder

COPY --from=pandoc /usr/bin/pandoc* /usr/bin/
RUN apk add --no-cache \
    gmp \
    libffi \
    lua5.3 \
    lua5.3-lpeg

COPY static-builder.sh pandoc.theme /data/
COPY pages /data/pages

RUN cd /data && /data/static-builder.sh

################################################################################
FROM python:3.8 AS recruiting-website-image-copyer

COPY --from=recruiting-website-static-builder /data/pages /data/pages
COPY --from=recruiting-website-static-builder /data/static /data/static
COPY image-copyer.py requirements.image-copyer.txt /data/

RUN pip install --no-cache-dir --requirement /data/requirements.image-copyer.txt
RUN python /data/image-copyer.py /data/static /data/pages

################################################################################
FROM python:3.8 AS recruiting-website-html-finalizer

COPY --from=recruiting-website-image-copyer /data/static /data/static
COPY html-finalizer.py requirements.html-finalizer.txt /data/

RUN pip install --no-cache-dir --requirement /data/requirements.html-finalizer.txt
RUN python /data/html-finalizer.py /data/static

################################################################################
FROM nginx:stable

COPY --from=recruiting-website-html-finalizer /data/static /usr/share/nginx/html
COPY nginx-default.conf /etc/nginx/conf.d/default.conf
COPY favicon.ico style.css /usr/share/nginx/html/
