from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound
from django.conf import settings
from django.contrib.auth.decorators import login_required

from .models import FavoriteGame
from gameMuster.games_manager import GamesManager

try:
    from gameMuster.mocked_data.mocked_games_manager import MockedGamesManager
except ImportError:
    pass


def get_list_of_filters(option, data_from_filter):
    return list(map(int, data_from_filter.getlist(option)))


def get_games_manager():
    return MockedGamesManager() if \
        settings.DEV_DATA_MODE else GamesManager()


def get_page_obj(request,
                 page_count,
                 obj_list):
    game_paginator = Paginator(obj_list, page_count)
    page_number = request.GET.get('page')
    page_obj = game_paginator.get_page(page_number)

    return page_obj


def get_favorite_games_id(request):
    return set(game.game_id for game
               in FavoriteGame.objects.filter(user=request.user))


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

    game_list = get_games_manager().generate_list_of_games(genres=chosen_params['genres'],
                                                           platforms=chosen_params['platforms'],
                                                           rating=chosen_params['rating'])

    platforms, genres = get_games_manager().get_list_of_filters()

    return render(request,
                  'gameMuster/index.html',
                  {'game_list': game_list,
                   'favorite_game_list': get_favorite_games_id(request)
                   if request.user.is_authenticated
                   else set(),
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
        game = get_games_manager().get_game_by_id(game_id)
    except LookupError as error:
        return HttpResponseNotFound(f'<h1>{error}</h1>')

    return render(request,
                  'gameMuster/detail.html',
                  {'game': game,
                   'tweet_list': game.tweets,
                   'game_name': game.name.replace(' ', '')})


@login_required
def favorite(request):
    favorite_games_id = FavoriteGame.objects.filter(user=request.user)
    favorite_games = [get_games_manager().get_game_by_id(game.game_id)
                      for game in favorite_games_id]

    return render(request,
                  'gameMuster/favorite_games.html',
                  {'game_list': favorite_games,
                   'favorite_game_list': get_favorite_games_id(request),
                   'page_obj': get_page_obj(request,
                                            4,
                                            favorite_games)})


@login_required
def add_to_favorite(request, game_id):
    current_favorite_game = FavoriteGame.all_objects.filter(game_id=game_id,
                                                            user=request.user).first()
    if not current_favorite_game:
        FavoriteGame.objects.create(game_id=game_id,
                                    user=request.user)
    else:
        current_favorite_game.restore()

    return redirect(request.META.get('HTTP_REFERER',
                                     'index'))


@login_required
def remove_from_favorite(request, game_id):
    favorite_game = FavoriteGame.objects.filter(game_id=game_id,
                                                user=request.user).first()
    if favorite_game:
        favorite_game.delete()

    return redirect(request.META.get('HTTP_REFERER',
                                     'index'))
