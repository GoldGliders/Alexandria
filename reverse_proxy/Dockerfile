FROM nginx

ADD ./conf.d/ /etc/nginx/conf.d/
COPY nginx.conf /etc/nginx/nginx.conf

RUN yum install -y \
    gettext
