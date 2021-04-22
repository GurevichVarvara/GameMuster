from django.db import models
from safedelete.models import SafeDeleteModel, SOFT_DELETE

from users.models import User


class FavoriteGame(SafeDeleteModel):
    """
    As we don't have any game model that's why
    to define what game was chosen we assume
    id from igdb
    """
    _safedelete_policy = SOFT_DELETE
    game_id = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

