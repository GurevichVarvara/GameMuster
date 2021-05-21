FROM python:3.9-slim-buster

EXPOSE 8000/tcp

RUN pip install --upgrade pip

COPY . /games
WORKDIR /games

RUN pip install -r requirements.txt

RUN chmod +x entrypoint.sh
ENTRYPOINT ["sh", "/games/entrypoint.sh"]
