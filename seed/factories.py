"""Factories for models"""
import factory
from faker import Factory

from gameMuster.models import Game, Platform, Genre

from users.models import User


faker = Factory.create()


class GameFactory(factory.django.DjangoModelFactory):
    """Game factory model"""
    class Meta:
        model = Game

    name = faker.name()
    game_id = faker.pyint()
    release_date = faker.date_time()
    img_url = faker.pystr(max_chars=10)
    description = faker.pystr(max_chars=10)
    user_rating = faker.pyint(min_value=50, max_value=100)
    user_rating_count = faker.pyint()
    critics_rating = faker.pyint(min_value=0, max_value=100)
    critics_rating_count = faker.pyint()

    @factory.post_generation
    def platforms(self, create, extracted):
        if not create:
            return
        if extracted:
            for platform in extracted:
                self.platforms.add(platform)

    @factory.post_generation
    def genres(self, create, extracted):
        if not create:
            return
        if extracted:
            for genre in extracted:
                self.platforms.add(genre)


class PlatformFactory(factory.django.DjangoModelFactory):
    """Platform factory model"""
    class Meta:
        model = Platform

    name = faker.name()


class GenreFactory(factory.django.DjangoModelFactory):
    """Genre factory model"""
    class Meta:
        model = Genre

    name = faker.name()


class UserFactory(factory.django.DjangoModelFactory):
    """User factory model"""
    class Meta:
        model = User

    username = faker.first_name()
    first_name = faker.first_name()
    last_name = faker.last_name()
    email = faker.email()
    active_time = faker.date_time()
