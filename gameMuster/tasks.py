from celery import shared_task

from gameMuster.game_managers.games_manager import games_manager
from gameMuster.models import Game


@shared_task
def refresh_games():
    if Game.objects.all():
        latest_game = Game.objects.exclude(release_date=None).order_by('-release_date')[0]
        last_release_date = latest_game.release_date
        print(latest_game)
    else:
        last_release_date = None

    games_manager.generate_list_of_games(last_release_date=last_release_date,
                                         count_of_games=10)
