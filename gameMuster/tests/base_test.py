"""Base test class"""
import os

from django.test import TestCase


class BaseTest(TestCase):
    """Base test class"""
    game_data_path = os.path.join(os.path.dirname(__file__), 'game_data.pickle')

    def check_list(self, container, target_class):
        """Test elements in the list to be instances of specified class"""
        self.assertIsInstance(container, list)

        for item in container:
            self.assertIsInstance(item, target_class)
