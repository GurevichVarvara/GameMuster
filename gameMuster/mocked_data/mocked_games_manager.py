import pickle
from pathlib import Path
from gameMuster.temp_models import Game


class MockedGamesManager:

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

    @staticmethod
    def _create_game_from_igdb_response(response_game):
        return Game(response_game['id'], response_game['name'], response_game['cover'],
                    response_game['genres'], response_game['summary'],
                    response_game['release_dates'], response_game['rating'],
                    response_game['rating_count'], response_game['aggregated_rating'],
                    response_game['aggregated_rating_count'],
                    screenshots=response_game['screenshots'],
                    platforms=response_game['platforms'],
                    tweets=[])

    @staticmethod
    def if_game_suits_filters(game_params,
                              filter_ids,
                              filter_map):
        if not filter_ids:
            return True

        if not game_params:
            return False

        filter_ids = set(filter_ids)
        filter_names = list(map(lambda x: x['name'],
                                filter(lambda x: x['id'] in filter_ids, filter_map)))

        return len(set(filter_names) & set(game_params)) > 0

    def generate_list_of_games(self, genres=None, platforms=None, rating=None):
        return [game for game in self.games if self.if_game_suits_filters(game.genres,
                                                                          genres,
                                                                          self.all_genres) and
                self.if_game_suits_filters(game.platforms,
                                           platforms,
                                           self.all_platforms) and
                (game.user_rating >= rating if rating else True)]

    def get_list_of_filters(self):
        return self.all_platforms, self.all_genres

    def get_game_by_id(self, game_id):
        game = list(filter(lambda x: x.game_id == game_id, self.games))

        if not len(game):
            raise LookupError('Game not found')

        return game[0]
