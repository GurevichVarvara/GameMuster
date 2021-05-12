from rest_framework import viewsets
from rest_framework import generics

from gameMuster.models import Game, Platform, Genre, Screenshot
from gameMuster.api.serializers import GameSerializer, PlatformSerializer, GenreSerializer, ScreenshotSerializer


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
    queryset = Screenshot.objects.all()
    serializer_class = ScreenshotSerializer

    def get_queryset(self):
        """
        This view should return a list of all the screenshots
        after filtering against a `game` query parameter
        """
        queryset = Screenshot.objects.all()
        game = self.request.query_params.get('game')

        if game:
            queryset = queryset.filter(game__id=game)

        return queryset


class ScreenshotDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Screenshot
    serializer_class = ScreenshotSerializer
