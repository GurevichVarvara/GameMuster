#!/bin/sh

docker-compose run web python manage.py migrate
