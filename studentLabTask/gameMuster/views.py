from django.shortcuts import render
from django.core.paginator import Paginator
from gameMuster.temp_models import Game


def index(request):
    game_list = [Game('PACKMAN',
                      'https://i1.sndcdn.com/avatars-000527330727-10g55j-t240x240.jpg',
                      'Arcade',
                      'Oldschool')] * 10
    game_paginator = Paginator(game_list, 4)

    page_number = request.GET.get('page')
    page_obj = game_paginator.get_page(page_number)

    return render(request, 'gameMuster/index.html', {'game_list': game_list,
                                                     'page_obj': page_obj})


def detail(request):
    return render(request, 'gameMuster/detail.html')