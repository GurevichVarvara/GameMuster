from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'gameMuster/index.html')


def detail(request):
    pass