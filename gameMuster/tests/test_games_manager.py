"""Games manager tests"""
from gameMuster.tests.base_test import BaseTest
from gameMuster.game_managers.games_manager import games_manager


class GamesManagerTestCase(BaseTest):
    """Games manager tests"""
    def test_generate_list_of_games(self):
        """Test that method returns list of Game instances"""
        games = games_manager.generate_list_of_games()

    def test_create_tweets_by_game_name(self):
        """Test that method returns list of Tweet instances"""
        tweets = games_manager.create_tweets_by_game_name(self.game)
