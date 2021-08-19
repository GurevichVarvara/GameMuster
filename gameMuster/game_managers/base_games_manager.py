"""Base game manager"""
from gameMuster.models import Platform, Genre, Game, Screenshot


class BaseGameManager:
    """Base game manager"""

    @staticmethod
    def _create_game_from_igdb_response(response_game):
        stored_game = Game.objects.filter(game_id=response_game["id"]).first()

        if stored_game:
            return stored_game

        game = Game.objects.create(
            game_id=response_game.get("id"),
            name=response_game.get("name"),
            release_date=response_game.get("release_dates"),
            img_url=response_game.get("cover"),
            description=response_game.get("summary"),
            user_rating=response_game.get("rating"),
            user_rating_count=response_game.get("rating_count"),
            critics_rating=response_game.get("aggregated_rating"),
            critics_rating_count=response_game.get("aggregated_rating_count"),
        )

        for platform in response_game["platforms"] or []:
            game.platforms.add(Platform.objects.get_or_create(name=platform)[0])

        for genre in response_game["genres"] or []:
            game.genres.add(Genre.objects.get_or_create(name=genre)[0])

        for screenshot in response_game["screenshots"] or []:
            Screenshot.objects.create(game=game, img_url=screenshot)

        return game
