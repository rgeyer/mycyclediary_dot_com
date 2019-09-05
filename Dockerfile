FROM python:3
ENV PYTHONBUFFERED 1
RUN mkdir /code
RUN apt-get update && apt-get install -y sqlite3
WORKDIR /code
ADD . /code/
RUN pip install -r requirements/test.txt
# RUN pip install pathlib2 winpdb-reborn # Eventually get debugging working again.
