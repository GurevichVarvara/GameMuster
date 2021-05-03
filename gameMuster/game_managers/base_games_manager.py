from gameMuster.models import Platform, Genre, Game, Screenshot


class BaseGameManager:

    @staticmethod
    def _create_game_from_igdb_response(response_game):
        stored_game = Game.objects.filter(game_id=response_game['id']).first()

        if stored_game:
            return stored_game

        game = Game.objects.create(game_id=response_game['id'],
                                   name=response_game['name'],
                                   release_date=response_game['release_dates'],
                                   img_url=response_game['cover'],
                                   description=response_game['summary'],
                                   user_rating=response_game['rating'],
                                   user_rating_count=response_game['rating_count'],
                                   critics_rating=response_game['aggregated_rating'],
                                   critics_rating_count=response_game['aggregated_rating_count'])

        for platform in (response_game['platforms'] or []):
            game.platforms.add(Platform.objects.get_or_create(name=platform)[0])

        for genre in (response_game['genres'] or []):
            game.genres.add(Genre.objects.get_or_create(name=genre)[0])

        for screenshot in (response_game['screenshots'] or []):
            Screenshot.objects.create(game=game,
                                      img_url=screenshot)

        return game
