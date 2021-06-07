"""Celery task"""
from celery import shared_task

from gameMuster.game_managers.games_manager import games_manager
from gameMuster.models import Game


@shared_task
def refresh_games(count_of_games=30):
    """Refresh games by generating new ones by games manager"""
    latest_game = Game.objects.exclude(release_date=None).order_by('-release_date').first()
    last_release_date = latest_game.release_date if latest_game else None

    games_manager.generate_list_of_games(last_release_date=last_release_date,
                                         count_of_games=count_of_games)
