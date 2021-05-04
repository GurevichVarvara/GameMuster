from celery import shared_task

from gameMuster.game_managers.games_manager import games_manager


@shared_task
def refresh_games():
    games_manager.generate_list_of_games()
