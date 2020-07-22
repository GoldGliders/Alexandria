FROM python:3.8

# copy
COPY . /usr/src/app

# make file and directories
RUN mkdir "/var/log/flask/"
RUN touch "/var/log/flask/access.log"

# add user
ARG UID=1000
RUN useradd -m -u ${UID} alexandria

# install libraries
RUN apt-get update  && apt-get install -y \
    zbar-tools
RUN pip install -r /usr/src/app/requirements.txt

WORKDIR /usr/src/app

ENTRYPOINT ["uwsgi", "/usr/src/app/uwsgi.ini"]
