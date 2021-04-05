from django.shortcuts import render
from django.core.paginator import Paginator
from gameMuster.temp_models import ModelManager
from gameMuster.games_manager import GamesManager


def index(request):
    game_manager = GamesManager()
    game_list = game_manager.generate_list_of_games()

    game_paginator = Paginator(game_list, 4)
    page_number = request.GET.get('page')
    page_obj = game_paginator.get_page(page_number)

    platforms, genres = game_manager.get_list_of_filters()

    return render(request, 'gameMuster/index.html',
                  {'game_list': game_list,
                   'page_obj': page_obj,
                   'platforms_available': platforms,
                   'genres_available': genres})


def detail(request, game_id):
    game_manager = GamesManager()
    game = game_manager.get_description_of_game(game_id)

    return render(request, 'gameMuster/detail.html', {'game': game,
                                                      'tweet_list': game.tweets})