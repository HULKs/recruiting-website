FROM pandoc/core AS pandoc

################################################################################
FROM alpine AS recruiting-website-static-builder

COPY --from=pandoc /usr/bin/pandoc* /usr/bin/
RUN apk add --no-cache \
    gmp \
    libffi \
    lua5.3 \
    lua5.3-lpeg

RUN apk add --no-cache \
    tree

COPY static-builder.sh pandoc.theme /data/
COPY pages /data/pages

RUN tree /data && cd /data && /data/static-builder.sh && tree /data

################################################################################
# FROM nginx:stable

# COPY --from=recruiting-website-static-builder /data/static /usr/share/nginx/html
# COPY nginx-default.conf /etc/nginx/conf.d/default.conf
# COPY favicon.ico style.css /usr/share/nginx/html/
