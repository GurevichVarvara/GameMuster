from django.conf import settings

from gameMuster.api_wrappers.igdb_wrapper import IgdbWrapper
from gameMuster.api_wrappers.twitter_wrapper import TwitterWrapper
from gameMuster.models import Game, Platform, Genre, Tweet


class GamesManager:

    def __init__(self):
        self.igdb_wrapper = IgdbWrapper(settings.IGDB_CLIENT_ID,
                                        settings.IGDB_CLIENT_SECRET)
        self.twitter_wrapper = TwitterWrapper(settings.TWITTER_BEARER_TOKEN)

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(GamesManager,
                                 cls).__new__(cls)
        return cls.instance

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

        platforms = [Platform.objects.filter(name=platform).first()
                     if Platform.objects.filter(name=platform).first()
                     else Platform.objects.create(name=platform)
                     for platform in response_game['platforms']]

        genres = [Genres.objects.filter(name=genre).first()
                  if Genres.objects.filter(name=genre).first()
                  else Genres.objects.create(name=genre)
                  for genre in response_game['genres']]

        for platform in platforms:
            game.plaforms.add(platform)

        for genre in genres:
            game.genres.add(genre)

        return game

    def generate_list_of_games(self, genres=None, platforms=None, rating=None):
        games_from_igdb = self.igdb_wrapper.get_games(genres=genres,
                                                      platforms=platforms,
                                                      rating=rating)

        games = []
        for game_from_igdb in games_from_igdb:
            game = GamesManager._create_game_from_igdb_response(game_from_igdb)
            GamesManager._create_tweets_by_game_name(game)

            games.append(game)

        return games

    def _create_tweets_by_game_name(self, game, count_of_tweets=None):
        for tweet in self.twitter_wrapper.get_tweets_by_game_name(game.name,
                                                                  count_of_tweets):
            Tweet.objects.create(game=game,
                                 content=tweet['full_text'],
                                 publisher=tweet['user']['name'],
                                 date=tweet['created_at'])
