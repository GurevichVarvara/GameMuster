from django.db import models
from safedelete.models import SafeDeleteModel, SOFT_DELETE

from users.models import User


class FavoriteGame(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE
    game_id = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

