"""Base test class"""
import os
import pickle

from django.test import TestCase

from gameMuster.game_managers.games_manager import games_manager


class BaseTest(TestCase):
    """Base test class"""
    game_data_path = os.path.join(os.path.dirname(__file__), 'game_data.pickle')

    def check_list(self, container, target_class):
        """Test elements in the list to be instances of specified class"""
        self.assertIsInstance(container, list)

        for item in container:
            self.assertIsInstance(item, target_class)

    def get_game(self):
        with open(self.game_data_path, 'rb') as file:
            self.game_data = pickle.load(file)

        return games_manager._create_game_from_igdb_response(self.game_data)
