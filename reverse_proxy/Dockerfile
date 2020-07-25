FROM nginx:1.19.1

ADD ./conf.d/ /etc/nginx/conf.d/
COPY nginx.conf /etc/nginx/nginx.conf

RUN apt-get update \
    && apt-get install -y \
    gettext \
    openssl \
    certbot
