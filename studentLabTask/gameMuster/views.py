from django.shortcuts import render


def index(request):
    return render(request, 'gameMuster/index.html')


def detail(request):
    return render(request, 'gameMuster/detail.html')