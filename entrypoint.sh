#!/bin/sh

python manage.py migrate
python manage.py collectstatic

guricorn studentLabTask.wsgi:application --bind 0.0.0.0:8000