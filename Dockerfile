FROM pandoc/core AS pandoc

################################################################################
FROM alpine AS recruiting-website-static-builder

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
RUN python image-copyer.py static/index.html pages

################################################################################
# FROM nginx:stable

# COPY --from=recruiting-website-image-copyer /data/static /usr/share/nginx/html
# COPY nginx-default.conf /etc/nginx/conf.d/default.conf
# COPY favicon.ico style.css /usr/share/nginx/html/
