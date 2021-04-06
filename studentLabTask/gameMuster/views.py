from django.shortcuts import render
from django.core.paginator import Paginator
from gameMuster.games_manager import GamesManager


def add_option_to_chosen_params(params_from_filter,
                                option, chosen_params,
                                chosen_params_container):
    params_from_filter['filter[' + option + '][eq]'] = '(' + ','.join(chosen_params) + ')'

    for param in chosen_params:
        chosen_params_container[option].add(int(param))


def index(request):
    game_manager = GamesManager()
    data_from_filter = request.GET
    params_from_filter = {}
    chosen_params = {'platforms': set(),
                     'genres': set(),
                     'rating': 50}

    if 'platforms' in data_from_filter:
        add_option_to_chosen_params(params_from_filter,
                                    'platforms', data_from_filter.getlist('platforms'),
                                    chosen_params)

    if 'genres' in data_from_filter:
        add_option_to_chosen_params(params_from_filter,
                                    'genres', data_from_filter.getlist('genres'),
                                    chosen_params)

    if 'rating' in data_from_filter:
        chosen_params['rating'] = params_from_filter['filter[rating][gte]'] = int(data_from_filter['rating'])

    game_list = game_manager.generate_list_of_games(params_from_filter)

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
    game_manager = GamesManager()
    game = game_manager.get_description_of_game(game_id)

    return render(request, 'gameMuster/detail.html', {'game': game,
                                                      'tweet_list': game.tweets,
                                                      'game_name': game.name.replace(' ', '')})