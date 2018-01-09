#!/usr/bin/env bash
#docker-compose exec cyclediaryweb pip install -r requirements/test.txt
docker-compose exec cyclediaryweb coverage run /usr/local/bin/pytest
