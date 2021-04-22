from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from gameMuster.games_manager import GamesManager
from django.http import HttpResponseNotFound
from gameMuster.mocked_data.mocked_games_manager import MockedGamesManager
from django.conf import settings
from django.urls import reverse_lazy

from .models import FavoriteGame


def get_list_of_filters(option, data_from_filter):
    return list(map(int, data_from_filter.getlist(option)))


def get_games_manager():
    return MockedGamesManager() if \
        settings.DEV_DATA_MODE else GamesManager()


def index(request):
    game_manager = get_games_manager()
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

    game_list = game_manager.generate_list_of_games(genres=chosen_params['genres'],
                                                    platforms=chosen_params['platforms'],
                                                    rating=chosen_params['rating'])

    game_paginator = Paginator(game_list, 4)
    page_number = request.GET.get('page')
    page_obj = game_paginator.get_page(page_number)

    platforms, genres = game_manager.get_list_of_filters()

    return render(request, 'gameMuster/index.html',
                  {'game_list': game_list,
                   'page_obj': page_obj,
                   'platforms': platforms,
                   'genres': genres,
                   'platforms_chosen': chosen_params['platforms'],
                   'genres_chosen': chosen_params['genres'],
                   'rating': chosen_params['rating']})


def detail(request, game_id):
    try:
        game_manager = get_games_manager()
        game = game_manager.get_game_by_id(game_id)
    except LookupError as error:
        return HttpResponseNotFound(f'<h1>{error}</h1>')

    return render(request, 'gameMuster/detail.html', {'game': game,
                                                      'tweet_list': game.tweets,
                                                      'game_name': game.name.replace(' ', '')})


def add_to_favorite(request, game_id):
    if not FavoriteGame.objects.filter(game_id=game_id).first():
        FavoriteGame.objects.create(game_id=game_id,
                                    user=request.user)

    return redirect('index')
