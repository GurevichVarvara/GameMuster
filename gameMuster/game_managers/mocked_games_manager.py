import pickle
from pathlib import Path
import os

from gameMuster.game_managers.base_games_manager import BaseGameManager


class MockedGamesManager(BaseGameManager):

    def __init__(self):
        mocked_data = self._get_mocked_data()
        self.games = mocked_data['games']
        self.tweets = mocked_data['tweets']

    @staticmethod
    def get_data_from_pickle_file(file_path):
        with open(Path(__file__).resolve().parent /
                  os.path.join('../mocked_data', file_path), 'rb') as f:
            data = pickle.load(f)

        return data

    def _get_mocked_data(self):
        return {'games': self.get_data_from_pickle_file('../mocked_data/mocked_games.pickle'),
                'tweets': self.get_data_from_pickle_file('../mocked_data/mocked_tweets.pickle')}

    def generate_list_of_games(self,
                               genres=None,
                               platforms=None,
                               rating=None,
                               last_release_date=None,
                               count_of_games=None):
        games = []
        for game_from_igdb in self.games:
            game = self._create_game_from_igdb_response(game_from_igdb)['game']

            games.append(game)

        return games

    def create_tweets_by_game_name(self,
                                   game,
                                   count_of_tweets=None):
        return self.tweets

