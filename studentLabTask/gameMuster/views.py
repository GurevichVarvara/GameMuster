from django.shortcuts import render
from django.core.paginator import Paginator
from gameMuster.temp_models import ModelManager
from gameMuster.games_manager import GamesManager


def index(request):
    game_manager = GamesManager()
    game_manager.generate_games()
    game_list = []
    game_paginator = Paginator(game_list, 4)

    page_number = request.GET.get('page')
    page_obj = game_paginator.get_page(page_number)

    return render(request, 'gameMuster/index.html', {'game_list': game_list,
                                                     'page_obj': page_obj,
                                                     'platforms_available': ['PC', 'PS4'],
                                                     'platforms_not_available': ['PS5'],
                                                     'genres_available': ['Platformer'],
                                                     'genres_not_available': ['Arcade']})


def detail(request, game_id):
    game = ModelManager.get_temp_instance_of_game()

    return render(request, 'gameMuster/detail.html', {'game': game,
                                                      'tweet_list': game.tweets})