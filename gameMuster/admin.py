from django.contrib import admin

from .models import FavoriteGame


class FavoriteGameAdmin(admin.ModelAdmin):
    model = FavoriteGame
    list_display = ['game_id',
                    'user',
                    'deleted']


admin.site.register(FavoriteGame, FavoriteGameAdmin)
