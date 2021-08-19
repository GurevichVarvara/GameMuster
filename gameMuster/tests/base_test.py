"""Base test class"""
from django.test import Client
from django.test import TestCase
from django.test.client import RequestFactory

from seed.factories import GameFactory, PlatformFactory, GenreFactory


class BaseTest(TestCase):
    """Base test class"""

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

        self.game = GameFactory()
        self.platform = PlatformFactory()
        self.genre = GenreFactory()

        self.game.platforms.add(self.platform)
        self.game.genres.add(self.genre)
