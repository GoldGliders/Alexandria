FROM python:3.8

# copy
COPY ./requirements.txt /tmp

# make file and directories
RUN mkdir "/var/log/flask/"
RUN touch "/var/log/flask/access.log"

# add user
ARG UID=1000
RUN useradd -m -u ${UID} alexandria

# install libraries
RUN pip install -r /tmp/requirements.txt

WORKDIR /app

ENTRYPOINT ["uwsgi", "--ini", "/app/uwsgi.ini", "-d"]
