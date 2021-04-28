from django.db import models
from safedelete.models import SafeDeleteModel, SOFT_DELETE

from users.models import User


class Platform(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['name']


class Genre(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['name']


class Game(models.Model):
    game_id = models.IntegerField()
    name = models.CharField(max_length=30)
    must = models.BooleanField(default=False)
    release_date = models.DateTimeField()
    img_url = models.CharField(max_length=120)
    description = models.TextField()
    user_rating = models.DecimalField(max_digits=4,
                                      decimal_places=2)
    user_rating_count = models.IntegerField()
    critics_rating = models.DecimalField(max_digits=4,
                                         decimal_places=2)
    critics_rating_count = models.IntegerField()
    platforms = models.ManyToManyField(Platform)
    genres = models.ManyToManyField(Genre)


class Screenshot(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    img_url = models.CharField(max_length=120)


class Tweet(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    content = models.CharField(max_length=280)
    publisher = models.CharField(max_length=30)
    date = models.DateTimeField()


class FavoriteGame(SafeDeleteModel):
    """
    As we don't have any game model that's why
    to define what game was chosen we assume
    id from igdb
    """
    _safedelete_policy = SOFT_DELETE
    game_id = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

