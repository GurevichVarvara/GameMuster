# Game Muster

This is iTechArt internship task

The main goal is to develop architecture and code structuring skills :muscle:

## Overview

The site is created for those who’s looking for games to play. 

You can discover latest games selected by rating, genre and platform. Beautiful icon pics, tweets connected with that game and detailed description would help you to choose what game you are take a fancy :hearts: 

And this time the game you like won’t go out of your head, just click on must-button on a game preview card and it’d imminently be included to your favorite games page (still working on that, would appear soon :stuck_out_tongue_winking_eye:) 

## Technologies

- Python
- Django 
- HTML
- CSS
- [Internet Game Database](https://www.igdb.com/api) API 
- [Twitter](https://developer.twitter.com/en/docs) API

## Would be implemented 

- [Heroku](https://www.heroku.com/) deployment :cloud:
- REST API using DRF

## Run locally

Install dependencies from the requirements.txt:
```
$ pip install -r requirements.txt
```
After cloning repository and downloading dependencies you need to set environmental variables connected to:
- [Database](https://docs.djangoproject.com/en/3.2/ref/settings/#databases) (PostgreSQL is the default here):
  - DATABASE_NAME
  - DATABASE_USER
  - DATABASE_PASSWORD
  - DATABASE_HOST
  - DATABASE_PORT
- [Email you'd send confirmation letters from](https://docs.djangoproject.com/en/3.2/topics/email/#send-mail):
  - EMAIL_HOST
  - EMAIL_HOST_USER
  - EMAIL_HOST_PASSWORD
  - EMAIL_PORT
- IGDB API credentials: 
  - IGDB_CLIENT_ID
  - IGDB_CLIENT_SECRET
- Twitter API credentials:
  - TWITTER_BEARER_TOKEN

You could set the environmental variable by running the command:
```
$ export YOUR_VAR=value
```

Now you're ready to run the server: 
```
$ python manage.py runserver
```
