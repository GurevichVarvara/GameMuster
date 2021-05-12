from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required

from gameMuster.models import FavoriteGame, Game, Platform, Genre, Tweet, Screenshot
from gameMuster.game_managers.games_manager import games_manager


def get_list_of_filters(option, data_from_filter):
    return list(map(int, data_from_filter.getlist(option)))


def get_page_obj(request,
                 page_count,
                 obj_list):
    game_paginator = Paginator(obj_list, page_count)
    page_number = request.GET.get('page')
    page_obj = game_paginator.get_page(page_number)

    return page_obj


def get_favorite_games_ids(request):
    return [game.game.game_id for game
            in FavoriteGame.objects.filter(user=request.user)] \
        if request.user.is_authenticated else []


def get_game_genres(game_list):
    game_genres = {game.id: [genre.name for genre
                             in Genre.objects.filter(game=game)]
                   for game in game_list}

    return game_genres


def index(request):
    data_from_filter = request.GET
    chosen_params = {'platforms': None,
                     'genres': None,
                     'rating': 50}

    if 'platforms' in data_from_filter:
        chosen_params['platforms'] = get_list_of_filters('platforms', data_from_filter)

    if 'genres' in data_from_filter:
        chosen_params['genres'] = get_list_of_filters('genres', data_from_filter)

    if 'rating' in data_from_filter:
        chosen_params['rating'] = int(data_from_filter['rating'])

    game_list = Game.objects.all()
    game_genres = get_game_genres(game_list)

    if chosen_params['platforms']:
        game_list = game_list.filter(platforms__pk__in=chosen_params['platforms'])
    if chosen_params['genres']:
        game_list = game_list.filter(genres__pk__in=chosen_params['genres'])
    if chosen_params['rating']:
        game_list = game_list.filter(user_rating__gte=chosen_params['rating'])

    platforms = Platform.objects.all()
    genres = Genre.objects.all()

    return render(request,
                  'gameMuster/index.html',
                  {'game_list': game_list,
                   'game_genres': game_genres,
                   'favorite_game_list': get_favorite_games_ids(request),
                   'page_obj': get_page_obj(request,
                                            4,
                                            game_list),

                   'platforms': platforms,
                   'genres': genres,
                   'platforms_chosen': chosen_params['platforms'],
                   'genres_chosen': chosen_params['genres'],
                   'rating': chosen_params['rating']})


def detail(request, game_id):
    try:
        game = Game.objects.filter(game_id=game_id).first()
    except LookupError as error:
        return HttpResponseNotFound(f'<h1>{error}</h1>')

    return render(request,
                  'gameMuster/detail.html',
                  {'game': game,
                   'genres': list(Genre.objects.filter(game=game)),
                   'platforms': list(Platform.objects.filter(game=game)),
                   'tweets': games_manager.create_tweets_by_game_name(game, 5),
                   'screenshots': list(Screenshot.objects.filter(game=game)),
                   'game_name': game.name.replace(' ', '')})


@login_required
def favorite(request):
    favorite_games = [favorite_game.game for favorite_game
                      in FavoriteGame.objects.filter(user=request.user)]
    game_genres = get_game_genres(favorite_games)

    test = get_favorite_games_ids(request)

    return render(request,
                  'gameMuster/favorite_games.html',
                  {'game_list': favorite_games,
                   'game_genres': game_genres,
                   'favorite_game_list': get_favorite_games_ids(request),
                   'page_obj': get_page_obj(request,
                                            4,
                                            favorite_games)})


@login_required
def add_to_favorite(request, game_id):
    game = Game.objects.filter(game_id=game_id).first()
    current_favorite_game = FavoriteGame.all_objects.filter(game=game,
                                                            user=request.user).first()
    if not current_favorite_game:
        FavoriteGame.objects.create(game=game,
                                    user=request.user)
    else:
        current_favorite_game.restore()

    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def remove_from_favorite(request, game_id):
    game = Game.objects.filter(game_id=game_id).first()
    favorite_game = FavoriteGame.objects.filter(game=game,
                                                user=request.user).first()
    if favorite_game:
        favorite_game.delete()

    return redirect(request.META.get('HTTP_REFERER'))
