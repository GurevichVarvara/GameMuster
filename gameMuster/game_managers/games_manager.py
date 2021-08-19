"""IGDB API games manager"""
from django.conf import settings

from gameMuster.game_managers.mocked_games_manager import MockedGamesManager
from gameMuster.game_managers.base_games_manager import BaseGameManager
from gameMuster.api_wrappers.igdb_wrapper import IgdbWrapper
from gameMuster.api_wrappers.twitter_wrapper import TwitterWrapper
from gameMuster.models import Tweet


class GamesManager(BaseGameManager):
    """IGDB API games manager"""

    def __init__(self):
        self.igdb_wrapper = IgdbWrapper(
            settings.IGDB_CLIENT_ID, settings.IGDB_CLIENT_SECRET
        )
        self.twitter_wrapper = TwitterWrapper(settings.TWITTER_BEARER_TOKEN)

    def generate_list_of_games(
        self,
        genres=None,
        platforms=None,
        rating=None,
        last_release_date=None,
        count_of_games=None,
    ):
        """Return filtered games"""
        games_from_igdb = self.igdb_wrapper.get_games(
            genres=genres,
            platforms=platforms,
            rating=rating,
            last_release_date=last_release_date,
            count_of_games=count_of_games,
        )

        games = []
        for game_from_igdb in games_from_igdb:
            game = self._create_game_from_igdb_response(game_from_igdb)
            games.append(game)

        return games

    def create_tweets_by_game_name(self, game, count_of_tweets=None):
        """Return tweets related to game"""
        tweets = []
        response = self.twitter_wrapper.get_tweets_by_game_name(
            game.name, count_of_tweets
        )

        for tweet in response:
            tweets.append(
                Tweet(
                    content=tweet["full_text"],
                    publisher=tweet["user"]["name"],
                    date=tweet["created_at"],
                )
            )

        return tweets


games_manager = MockedGamesManager() if settings.DEV_DATA_MODE else GamesManager()
