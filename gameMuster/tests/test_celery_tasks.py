"""Celery tasks tests"""
import datetime

from django.test import TestCase

from gameMuster.tasks import refresh_games
from gameMuster.models import Game

LAST_RELEASE_DATE = datetime.date(2010, 1, 1)
COUNT_OF_GAMES_TO_LOAD = 30


class CeleryTasksTestCase(TestCase):
    """Celery tasks tests"""

    def test_refresh_games(self):
        """Test that method returns list of ordered by date games"""

        # Change last release date in database
        game = self.get_game()
        game.release_date = LAST_RELEASE_DATE
        game.save()

        games = refresh_games(COUNT_OF_GAMES_TO_LOAD)

        self.check_list(games, Game)
        self.assertGreaterEqual(COUNT_OF_GAMES_TO_LOAD, len(games))

        for new_game in games:
            self.assertGreater(new_game.release_date, game.release_date)
