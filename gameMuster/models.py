"""Related to games models"""
from datetime import datetime
from django.db import models

from users.models import User


class SoftDeletionQuerySet(models.QuerySet):
    """Queryset of soft delete model"""

    class Meta:
        abstract = True

    def alive(self):
        """Return only not deleted objects"""
        return self.filter(deleted=None)


class SoftDeleteManager(models.Manager):
    """Manager of soft delete model"""

    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop("alive_only", True)
        super(SoftDeleteManager, self).__init__(*args, **kwargs)

    class Meta:
        abstract = True

    def get_queryset(self):
        """Return either alive or all objects"""
        if self.alive_only:
            query_set = SoftDeletionQuerySet(self.model).alive()
        else:
            query_set = SoftDeletionQuerySet(self.model)

        return query_set


class SoftDeleteModel(models.Model):
    """Soft delete model"""

    deleted = models.DateTimeField(null=True, default=None)
    objects = SoftDeleteManager()
    all_objects = SoftDeleteManager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self):
        """Soft delete"""
        self.deleted = datetime.now()
        self.save()

    def hard_delete(self):
        """Permanent delete"""
        super(SoftDeleteModel, self).delete()

    def restore(self):
        """Restore soft deleted object"""
        self.deleted = None
        self.save()


class Platform(models.Model):
    """Platform model"""

    name = models.CharField(max_length=50)

    class Meta:
        ordering = ["name"]


class Genre(models.Model):
    """Genre model"""

    name = models.CharField(max_length=50)

    class Meta:
        ordering = ["name"]


class Game(models.Model):
    """Game model"""

    game_id = models.IntegerField()
    name = models.CharField(max_length=100)
    must = models.BooleanField(default=False)
    release_date = models.DateTimeField(null=True, default=None)
    img_url = models.CharField(max_length=120, null=True, default=None)
    description = models.TextField(null=True, default=None)
    user_rating = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, default=None
    )
    user_rating_count = models.IntegerField(null=True, default=None)
    critics_rating = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, default=None
    )
    critics_rating_count = models.IntegerField(null=True, default=None)
    platforms = models.ManyToManyField(Platform)
    genres = models.ManyToManyField(Genre)
    favorite_games = models.ManyToManyField(User, through="FavoriteGame")

    class Meta:
        ordering = ["release_date"]


class Screenshot(models.Model):
    """Screenshot model"""

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    img_url = models.CharField(max_length=120)


class FavoriteGame(SoftDeleteModel):
    """Favorite game model"""

    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)


class Tweet:
    """Tweet class"""

    def __init__(self, content, publisher, date):
        self.content = content
        self.publisher = publisher
        self.date = date
