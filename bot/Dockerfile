FROM python:3.8
COPY ./requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

RUN mkdir /app
RUN mkdir "/var/log/flask/"
RUN touch "/var/log/flask/access.log"

WORKDIR /app
COPY ./app.py /app/app.py

CMD ["flask", "run", "--host=0.0.0.0", "--port=4000"]
