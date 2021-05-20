FROM python:3.9-slim-buster

RUN pip install --upgrade pip

COPY . /games
WORKDIR /games

RUN pip install -r requirements.txt

RUN chmod +x entrypoint.sh
ENTRYPOINT ["sh", "/games/docker/celery_receiver/entrypoint.sh"]
