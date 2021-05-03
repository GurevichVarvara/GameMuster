from django.conf import settings

from gameMuster.models import Platform, Genre
from gameMuster.temp_models import Game, Tweet
from gameMuster.api_wrappers.igdb_wrapper import IgdbWrapper
from gameMuster.api_wrappers.twitter_wrapper import TwitterWrapper


class BaseGameManager:

    @staticmethod
    def _create_game_from_igdb_response(response_game):
        game = Game.objects.create(game_id=response_game['id'],
                                   name=response_game['name'],
                                   release_date=response_game['release_dates'],
                                   img_url=response_game['cover'],
                                   description=response_game['summary'],
                                   user_rating=response_game['rating'],
                                   user_rating_count=response_game['rating_count'],
                                   critics_rating=response_game['aggregated_rating'],
                                   critics_rating_count=response_game['aggregated_rating_count'])

        if response_game['platforms']:
            platforms = [Platform.objects.filter(name=platform).first()
                         if Platform.objects.filter(name=platform).first()
                         else Platform.objects.create(name=platform)
                         for platform in response_game['platforms']]

            game.platforms.add(*platforms)

        if response_game['genres']:
            genres = [Genre.objects.filter(name=genre).first()
                      if Genre.objects.filter(name=genre).first()
                      else Genre.objects.create(name=genre)
                      for genre in response_game['genres']]

            game.genres.add(*genres)

        return game

    def _create_tweets_by_game_name(self, game, count_of_tweets=None):
        for tweet in self.twitter_wrapper.get_tweets_by_game_name(game.name,
                                                                  count_of_tweets):
            Tweet.objects.create(game=game,
                                 content=tweet['full_text'],
                                 publisher=tweet['user']['name'],
                                 date=tweet['created_at'])


class GamesManager(BaseGameManager):

    def __init__(self):
        self.igdb_wrapper = IgdbWrapper(settings.IGDB_CLIENT_ID,
                                        settings.IGDB_CLIENT_SECRET)
        self.twitter_wrapper = TwitterWrapper(settings.TWITTER_BEARER_TOKEN)

    def generate_list_of_games(self,
                               genres=None,
                               platforms=None,
                               rating=None,
                               last_release_date=None):
        games_from_igdb = self.igdb_wrapper.get_games(genres=genres,
                                                      platforms=platforms,
                                                      rating=rating)

        games = []
        for game_from_igdb in games_from_igdb:
            game = self._create_game_from_igdb_response(game_from_igdb)
            GamesManager._create_tweets_by_game_name(game)

            games.append(game)

        return games
