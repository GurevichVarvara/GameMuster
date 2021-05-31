"""Admin configuration module"""
from django.contrib import admin

from .models import FavoriteGame


class FavoriteGameAdmin(admin.ModelAdmin):
    """Describe how to represent favorite game on admin page"""
    model = FavoriteGame
    list_display = ['game_id',
                    'user',
                    'deleted']


admin.site.register(FavoriteGame, FavoriteGameAdmin)
