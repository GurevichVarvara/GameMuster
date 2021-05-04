from django.db import models

from datetime import datetime

from users.models import User


class SoftDeletionQuerySet(models.QuerySet):

    class Meta:
        abstract = True

    def alive(self):
        return self.filter(deleted=None)


class SoftDeleteManager(models.Manager):

    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(SoftDeleteManager, self).__init__(*args, **kwargs)

    class Meta:
        abstract = True

    def get_queryset(self):
        if self.alive_only:
            query_set = SoftDeletionQuerySet(self.model).alive()
        else:
            query_set = SoftDeletionQuerySet(self.model)

        return query_set


class SoftDeleteModel(models.Model):

    deleted = models.DateTimeField(null=True,
                                   default=None)
    objects = SoftDeleteManager()
    all_objects = SoftDeleteManager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self):
        self.deleted = datetime.now()
        self.save()

    def hard_delete(self):
        super(SoftDeleteModel, self).delete()

    def restore(self):
        self.deleted = None
        self.save()


class FavoriteGame(SoftDeleteModel):
    """
    As we don't have any game model that's why
    to define what game was chosen we assume
    id from igdb
    """
    game_id = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
