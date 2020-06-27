FROM nginx

ADD ./conf.d/ /etc/nginx/conf.d/
COPY nginx.conf /etc/nginx/nginx.conf

CMD ["/usr/sbin/nginx", "-g", "daemon off;"]
