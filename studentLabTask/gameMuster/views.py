from django.shortcuts import render
from django.core.paginator import Paginator
from gameMuster.temp_models import ModelManager


def index(request):
    game_list = [ModelManager.get_temp_instance_of_game()] * 10
    game_paginator = Paginator(game_list, 4)

    page_number = request.GET.get('page')
    page_obj = game_paginator.get_page(page_number)

    return render(request, 'gameMuster/index.html', {'game_list': game_list,
                                                     'page_obj': page_obj})


def detail(request, game_id):

    return render(request, 'gameMuster/detail.html')