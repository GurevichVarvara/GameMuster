"""Base test class"""

from django.test import Client
from django.test import TestCase
from django.test.client import RequestFactory

from seed.factories import GameFactory, PlatformFactory, GenreFactory, UserFactory


USER_PASSWORD = "11111"


class BaseTest(TestCase):
    """Base test class"""

    def setUp(self):
        self.client = Client()
        self.user_password = USER_PASSWORD
        self.user = self._create_user()
        self.factory = RequestFactory()

        self.game = GameFactory()
        self.platform = PlatformFactory()
        self.genre = GenreFactory()

        self.game.platforms.add(self.platform)
        self.game.genres.add(self.genre)

    def _create_user(self):
        user = UserFactory()

        user.set_password(self.user_password)
        user.save()

        return user

    def login_user(self):
        if not self.user:
            self._create_user()

        return self.client.login(
            username=self.user.username, password=self.user_password
        )
