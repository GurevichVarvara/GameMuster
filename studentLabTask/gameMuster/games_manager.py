import os
from gameMuster.temp_models import Game, Tweet
from gameMuster.api_wrappers.igdb_wrapper import IgdbWrapper
from gameMuster.api_wrappers.twitter_wrapper import TwitterWrapper

IGDB_CLIENT_ID = os.environ.get('IGDB_CLIENT_ID')
IGDB_CLIENT_SECRET = os.environ.get('IGDB_CLIENT_SECRET')
TWITTER_BEARER_TOKEN = os.environ.get('TWITTER_BEARER_TOKEN')


class GamesManager:

    def __init__(self):
        self.igdb_wrapper = IgdbWrapper(IGDB_CLIENT_ID, IGDB_CLIENT_SECRET)
        self.twitter_wrapper = TwitterWrapper(TWITTER_BEARER_TOKEN)

    def create_game_from_igdb_response(self, response_game):
        return Game(response_game['id'], response_game['name'], response_game['cover'],
                    response_game['genres'], response_game['summary'],
                    response_game['release_dates'], response_game['rating'],
                    response_game['rating_count'], response_game['aggregated_rating'],
                    response_game['aggregated_rating_count'],
                    screenshots=response_game['screenshots'],
                    platforms=response_game['platforms'],
                    tweets=self.get_tweets_by_game_name(response_game['name']))

    def generate_list_of_games(self, params_from_filter):
        games = self.igdb_wrapper.get_games(params_from_filter)

        return [self.create_game_from_igdb_response(game) for game in games]

    def get_game_by_id(self, game_id):
        game = self.igdb_wrapper.get_games({'filter[id][eq]': game_id})[0]

        return self.create_game_from_igdb_response(game)

    def get_list_of_filters(self):
        params = {'fields': 'name'}
        platforms = self.igdb_wrapper.get_platforms(params)
        genres = self.igdb_wrapper.get_genres(params)

        return platforms, genres

    @staticmethod
    def create_tweet_from_twitter_response(response_tweet):
        return Tweet(response_tweet['full_text'],
                     response_tweet['created_at'],
                     response_tweet['user']['name'])

    def get_tweets_by_game_name(self, game_name, count_of_tweets=None):
        return [self.create_tweet_from_twitter_response(tweet)
                for tweet in self.twitter_wrapper.get_tweets_by_game_name(game_name,
                                                                          count_of_tweets)]
