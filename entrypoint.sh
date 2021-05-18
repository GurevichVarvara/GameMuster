#!/bin/sh

python3 manage.py migrate
python3 manage.py collectstatic

exec gunicorn studentLabTask.wsgi:application --bind 0.0.0.0:8000 --reload