"""Mocked data games manager"""
import pickle
from pathlib import Path
import os

from gameMuster.game_managers.base_games_manager import BaseGameManager
from gameMuster.models import Tweet


class MockedGamesManager(BaseGameManager):
    """Mocked data games manager"""

    def __init__(self):
        mocked_data = self._get_mocked_data()
        self.games = mocked_data["games"]
        self.tweets = mocked_data["tweets"]

    @staticmethod
    def get_data_from_pickle_file(file_path):
        """Return data from pickle file from mocked_data folder"""
        with open(
            Path(__file__).resolve().parent / os.path.join("../mocked_data", file_path),
            "rb",
        ) as file:
            data = pickle.load(file)

        return data

    def _get_mocked_data(self):
        return {
            "games": self.get_data_from_pickle_file("mocked_games.pickle"),
            "tweets": self.get_data_from_pickle_file("mocked_tweets.pickle"),
        }

    def generate_list_of_games(
        self,
        genres=None,
        platforms=None,
        rating=None,
        last_release_date=None,
        count_of_games=None,
    ):
        """Return all games"""
        return [
            self._create_game_from_igdb_response(game_from_igdb)
            for game_from_igdb in self.games
        ]

    def create_tweets_by_game_name(self, game, count_of_tweets=None):
        """Return all tweets"""
        return [
            Tweet(
                content=tweet["full_text"],
                publisher=tweet["user"]["name"],
                date=tweet["created_at"],
            )
            for tweet in self.tweets
        ]
