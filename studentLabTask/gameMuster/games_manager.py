import requests
from gameMuster.temp_models import Game, Tweet
import os
import datetime
from gameMuster.api_wrappers.igdb_wrapper import IgdbWrapper

IGDB_CLIENT_ID = os.environ.get('IGDB_CLIENT_ID')
IGDB_CLIENT_SECRET = os.environ.get('IGDB_CLIENT_SECRET')
TWITTER_BEARER_TOKEN = os.environ.get('TWITTER_BEARER_TOKEN')

# Would be removed after creating a DB
games_storage = {}


class GamesManager:

    def __init__(self):
        self.igdb_wrapper = IgdbWrapper(IGDB_CLIENT_ID, IGDB_CLIENT_SECRET)
        self.twitter_search_url = 'https://api.twitter.com/1.1/search/tweets.json'
        self.twitter_header = self._get_access_twitter_token()
        self.game_params = {'fields': 'id, name, cover.image_id, genres.name,'
                                      'summary, release_dates,'
                                      'aggregated_rating,'
                                      'aggregated_rating_count,'
                                      'rating, rating_count,'
                                      'screenshots.image_id,'
                                      'platforms.name',
                            'filter[cover][not_eq]': 'null',
                            'filter[genres][not_eq]': 'null',
                            'filter[screenshots][not_eq]': 'null'}

    @staticmethod
    def _get_access_twitter_token():
        return {'Authorization': 'Bearer {}'.format(TWITTER_BEARER_TOKEN)}

    def generate_list_of_games(self, params_from_filter):
        games = self.igdb_wrapper.get_games({**self.game_params, **params_from_filter})

        return [Game(game['id'], game['name'], game['cover'],
                     game['genres'], game['summary'],
                     game['release_dates'], game['rating'],
                     game['rating_count'], game['aggregated_rating'],
                     game['aggregated_rating_count'],
                     screenshots=game['screenshots'],
                     platforms=game['platforms'],
                     tweets=self.get_tweets_by_game_name(game['name']))
                for game in games]

    def get_game_by_id(self, game_id):
        game = self.igdb_wrapper.get_games({**self.game_params, **{'filter[id][eq]': game_id}})[0]

        return Game(game['id'], game['name'], game['cover'],
                    game['genres'], game['summary'],
                    game['release_dates'], game['rating'],
                    game['rating_count'], game['aggregated_rating'],
                    game['aggregated_rating_count'],
                    screenshots=game['screenshots'],
                    platforms=game['platforms'],
                    tweets=self.get_tweets_by_game_name(game['name']))

    def get_list_of_filters(self):
        params = {'fields': 'name'}
        platforms = self.igdb_wrapper.get_platforms(params)
        genres = self.igdb_wrapper.get_genres(params)

        return platforms, genres

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
                      result_tweet['user']['name'])
                for result_tweet in result_tweets]
