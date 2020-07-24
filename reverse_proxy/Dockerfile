FROM nginx:1.19.1

ADD ./conf.d/ /etc/nginx/conf.d/
COPY nginx.conf /etc/nginx/nginx.conf
RUN mkdir -p /etc/www/html/.well-known/acme-challenge
RUN echo "success" > /etc/www/html/.well-known/acme-challenge/test.txt

RUN apt-get update \
    && apt-get install -y \
    gettext
