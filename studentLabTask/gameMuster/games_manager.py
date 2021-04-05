from django.shortcuts import get_object_or_404
import requests
from gameMuster.temp_models import Game, Tweet
import os
import datetime

IGDB_CLIENT_ID = os.environ.get('IGDB_CLIENT_ID')
IGDB_CLIENT_SECRET = os.environ.get('IGDB_CLIENT_SECRET')

# Would be removed after creating a DB
games_storage = {}


class GamesManager:

    def __init__(self):
        self.igdb_main_url = 'https://api.igdb.com/v4/'
        self.igdb_header = self._get_access_igdb_token()

    @staticmethod
    def _get_access_igdb_token():
        print(IGDB_CLIENT_ID)
        print(IGDB_CLIENT_SECRET)
        access_token = requests.post('https://id.twitch.tv/oauth2/'
                                     'token?client_id={}&client_secret'
                                     '={}&grant_type=client_credentials'.format(
                                        IGDB_CLIENT_ID,
                                        IGDB_CLIENT_SECRET)).json()['access_token']

        return {'Client-ID': IGDB_CLIENT_ID,
                'Authorization': 'Bearer {}'.format(access_token)}

    def _get_api_response(self, access_token_func, url, headers, params):
        response_from_api = requests.post(url, headers=headers, params=params)

        # if access token has expired
        if response_from_api.status_code != 200:
            self.igdb_header = access_token_func()
            response_from_api = requests.post(url, headers=headers, params=params)

        return response_from_api.json()

    @staticmethod
    def _get_img(img_id):
        return 'https://images.igdb.com/igdb/image/upload/t_cover_big/{}.jpg'.format(img_id)

    def generate_list_of_games(self):
        params = {'fields': 'id, name, cover.image_id, genres.name',
                  'filter[cover][not_eq]': 'null',
                  'filter[genres][not_eq]': 'null',
                  'filter[screenshots][not_eq]': 'null'}
        result_games = self._get_api_response(self._get_access_igdb_token,
                                              self.igdb_main_url + 'games/',
                                              self.igdb_header,
                                              params)

        games = []
        for game in result_games:
            game = Game(game['id'],
                        game['name'],
                        self._get_img(game['cover']['image_id']),
                        [genre['name'] for genre in game['genres']])

            games.append(game)
            games_storage[game.game_id] = game

        return games

    def get_list_of_filters(self):
        params = {'fields': 'name'}
        result_platforms = self._get_api_response(self._get_access_igdb_token,
                                                  self.igdb_main_url + 'platforms/',
                                                  self.igdb_header,
                                                  params)
        result_genres = self._get_api_response(self._get_access_igdb_token,
                                               self.igdb_main_url + 'genres/',
                                               self.igdb_header,
                                               params)

        return ([platform['name'] for platform in result_platforms],
                [genre['name'] for genre in result_genres])

    def get_description_of_game(self, game_id):
        game = games_storage[game_id]

        params = {'fields': 'summary, release_dates,'
                            'aggregated_rating,'
                            'aggregated_rating_count,'
                            'rating, rating_count,'
                            'screenshots.image_id,'
                            'platforms.name',
                  'filter[id][eq]': game_id}
        result_game = self._get_api_response(self._get_access_igdb_token,
                                             self.igdb_main_url + 'games/',
                                             self.igdb_header,
                                             params)[0]

        release_date = datetime.datetime.fromtimestamp(result_game['release_dates'][0]) \
                        if 'release_dates' in result_game else 'no release date'
        tweets = [Tweet(
            'In 1999, Billy Mitchell of Hollywood, Florida became the first person to obtain a perfect score '
            'of 3,333,360 at Pac-Man, eating every possible dot, energizer, ghost, and bonus on every level '
            'without losing a single life in the process.',
            datetime.datetime.now(),
            'somebody')] * 3
        game.set_full_description(result_game['summary'],
                                  release_date,
                                  result_game.get('rating', 0),
                                  result_game.get('rating_count', 0),
                                  result_game.get('aggregated_rating', 0),
                                  result_game.get('aggregated_rating_count', 0),
                                  screenshots=[self._get_img(screenshot['image_id']) \
                                               for screenshot in result_game['screenshots']],
                                  platforms=[platform['name'] for platform \
                                             in result_game['platforms']],
                                  tweets=tweets)

        return game









