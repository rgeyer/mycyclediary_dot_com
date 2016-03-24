FROM python:2.7
ENV PYTHONBUFFERED 1
RUN mkdir /code
RUN apt-get update && apt-get install -y sqlite3 cron
WORKDIR /code
ADD . /code/
RUN pip install -r requirements.txt

ADD dockerfiles/stravasync.cron /etc/cron.d/stravasync
RUN chmod 0744 /etc/cron.d/stravasync
RUN touch /var/log/cron.log
