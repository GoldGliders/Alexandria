FROM nginx

ADD ./conf.d/ /etc/nginx/conf.d/
COPY nginx.conf /etc/nginx/nginx.conf

RUN apt-get install -y \
    gettext
