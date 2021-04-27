from django.db import models
from safedelete.models import SafeDeleteModel, SOFT_DELETE

from users.models import User


class Game(models.Model):
    game_id = models.IntegerField()
    name = models.CharField(max_length=30)
    release_date = model.DateTimeField()
    must = model.BooleanField()
    img_url = models.CharField(max_length=120)
    description = models.TextField()
    user_rating = models.DecimalField()
    user_rating_count = models.IntegerField()
    critics_rating = models.DecimalField()
    critics_rating_count = models.IntegerField()
    

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

