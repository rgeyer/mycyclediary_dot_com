#FROM python:2.7
#ENV PYTHONBUFFERED 1
#RUN mkdir /code
#RUN apt-get update && apt-get install -y sqlite3
#WORKDIR /code
#ADD . /code/
#RUN pip install -r requirements/test.txt

#ADD dockerfiles/stravasync.cron /etc/cron.d/stravasync
#RUN chmod 0744 /etc/cron.d/stravasync
#RUN touch /var/log/cron.log


FROM python:3
ENV PYTHONBUFFERED 1
RUN mkdir /code
RUN apt-get update && apt-get install -y sqlite3
WORKDIR /code
ADD . /code/
RUN pip install -r requirements/test.txt && \
  cd /tmp && \
  curl -O https://versaweb.dl.sourceforge.net/project/winpdb/winpdb/winpdb1.4.6/winpdb-1.4.6.tar.gz && \
  tar -zxf winpdb-1.4.6.tar.gz && \
  cd winpdb-1.4.6 && \
  python setup.py install -f && \
  easy_install pudb
