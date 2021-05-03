import pickle
from pathlib import Path

from gameMuster.games_manager import BaseGameManager
from gameMuster.models import Game


class MockedGamesManager(BaseGameManager):

    def __init__(self):
        mocked_data = self._get_mocked_data()
        self.games = [self._create_game_from_igdb_response(game)
                      for game in mocked_data['games']]
        self.all_platforms = mocked_data['all_platforms']
        self.all_genres = mocked_data['all_genres']

    @staticmethod
    def get_data_from_pickle_file(file_path):
        with open(Path(__file__).resolve().parent /
                  file_path, 'rb') as f:
            data = pickle.load(f)

        return data

    def _get_mocked_data(self):
        return {'games': self.get_data_from_pickle_file('mocked_games.pickle'),
                'all_platforms': self.get_data_from_pickle_file('mocked_all_platforms.pickle'),
                'all_genres': self.get_data_from_pickle_file('mocked_all_genres.pickle')}

    def generate_list_of_games(self, last_release_date):
        games = []
        for game_from_igdb in self.games:
            if game_from_igdb['release_dates'] > last_release_date:
                continue

            game = self._create_game_from_igdb_response(game_from_igdb)
            self._create_tweets_by_game_name(game)

            games.append(game)

        return games
