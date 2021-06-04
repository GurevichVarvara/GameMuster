"""Games manager tests"""
import os
import pickle

from django.test import TestCase
from gameMuster.models import Game, Tweet
from gameMuster.game_managers.games_manager import games_manager

GAME_DATA_FILENAME = os.path.join(os.path.dirname(__file__), 'game_data.pickle')


class GamesManagerTestCase(TestCase):

    def setUp(self):
        with open(GAME_DATA_FILENAME, 'rb') as file:
            self.game_data = pickle.load(file)

        self.game = games_manager._create_game_from_igdb_response(self.game_data)

    def check_list(self, container, target_class):
        self.assertIsInstance(container, list)

        for item in container:
            self.assertIsInstance(item, target_class)

    def test_create_game_from_igdb_response(self):
        """Test that method creates Game instance"""
        game = games_manager._create_game_from_igdb_response(self.game_data)

        self.assertIsInstance(game, Game)

    def test_generate_list_of_games(self):
        """Test that method returns list of Game instances"""
        games = games_manager.generate_list_of_games()

        self.check_list(games, Game)

    def test_create_tweets_by_game_name(self):
        """Test that method returns list of Tweet instances"""
        tweets = games_manager.create_tweets_by_game_name(self.game)

        self.check_list(tweets, Tweet)
