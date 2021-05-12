from rest_framework import viewsets
from rest_framework import generics

from gameMuster.models import Game, Platform, Genre, Screenshot, FavoriteGame
from gameMuster.api.serializers import GameSerializer, PlatformSerializer, \
    GenreSerializer, ScreenshotSerializer, FavoriteGameSerializer


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Game
    serializer_class = GameSerializer


class PlatformViewSet(viewsets.ModelViewSet):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer


class PlatformDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Platform
    serializer_class = PlatformSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class GenreDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Genre
    serializer_class = GenreSerializer


class ScreenshotViewSet(viewsets.ModelViewSet):
    serializer_class = ScreenshotSerializer

    def get_queryset(self):
        queryset = Screenshot.objects.all()
        game = self.request.query_params.get('game')

        if game:
            queryset = queryset.filter(game__id=game)

        return queryset


class ScreenshotDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Screenshot
    serializer_class = ScreenshotSerializer


class FavoriteGameViewSet(viewsets.ModelViewSet):
    serializer_class = ScreenshotSerializer

    def get_queryset(self):
        queryset = FavoriteGame.objects.all()
        username = self.request.query_params.get('username')

        if username:
            queryset = queryset.filter(user__name=username)

        return queryset


class FavoriteGameDetail(generics.RetrieveUpdateDestroyAPIView):
    model = FavoriteGame
    serializer_class = FavoriteGameSerializer
