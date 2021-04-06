import requests
from gameMuster.temp_models import Game, Tweet
import os
import datetime

IGDB_CLIENT_ID = os.environ.get('IGDB_CLIENT_ID')
IGDB_CLIENT_SECRET = os.environ.get('IGDB_CLIENT_SECRET')
TWITTER_BEARER_TOKEN = os.environ.get('TWITTER_BEARER_TOKEN')

# Would be removed after creating a DB
games_storage = {}


class GamesManager:

    def __init__(self):
        self.igdb_main_url = 'https://api.igdb.com/v4/'
        self.igdb_header = self._get_access_igdb_token()
        self.twitter_search_url = 'https://api.twitter.com/1.1/search/tweets.json'
        self.twitter_header = self._get_access_twitter_token()

    @staticmethod
    def _get_access_igdb_token():
        access_token = requests.post('https://id.twitch.tv/oauth2/'
                                     'token?client_id={}&client_secret'
                                     '={}&grant_type=client_credentials'.format(
                                        IGDB_CLIENT_ID,
                                        IGDB_CLIENT_SECRET)).json()['access_token']

        return {'Client-ID': IGDB_CLIENT_ID,
                'Authorization': 'Bearer {}'.format(access_token)}

    @staticmethod
    def _get_access_twitter_token():
        return {'Authorization': 'Bearer {}'.format(TWITTER_BEARER_TOKEN)}

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
        for result_game in result_games:
            game = Game(result_game['id'],
                        result_game['name'],
                        self._get_img(result_game['cover']['image_id']),
                        [genre['name'] for genre in result_game['genres']])

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

    def get_tweets_by_game_name(self, game_name, count_of_tweets=3):
        params = {'q': '%23{}'.format(game_name.replace(' ', '')),
                  'tweet_mode': 'extended',
                  'tweet.fields': 'full_text, created_at, user.name',
                  'count': count_of_tweets}
        result_tweets = requests.get(self.twitter_search_url,
                                     headers=self.twitter_header,
                                     params=params).json()['statuses']

        return [Tweet(result_tweet['full_text'],
                      datetime.datetime.strptime(result_tweet['created_at'],
                                                 '%a %b %d %H:%M:%S %z %Y'),
                      result_tweet['user']['name']) \
                for result_tweet in result_tweets]

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

        game.set_full_description(result_game['summary'],
                                  release_date,
                                  round(result_game.get('rating', 0), 1),
                                  result_game.get('rating_count', 0),
                                  round(result_game.get('aggregated_rating', 0), 1),
                                  result_game.get('aggregated_rating_count', 0),
                                  screenshots=[self._get_img(screenshot['image_id']) \
                                               for screenshot in result_game['screenshots']],
                                  platforms=[platform['name'] for platform \
                                             in result_game['platforms']],
                                  tweets=self.get_tweets_by_game_name(game.name))

        return game









