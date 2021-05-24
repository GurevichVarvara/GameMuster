from rest_framework import viewsets
from rest_framework import generics
from rest_framework.response import Response

from gameMuster.models import Game, Platform, Genre, Screenshot, FavoriteGame
from api.serializers import GameSerializer, PlatformSerializer, \
    GenreSerializer, ScreenshotSerializer, FavoriteGameSerializer, \
    TweetSerializer, UserSerializer
from gameMuster.game_managers.games_manager import games_manager
from users.models import User
from users.views import send_confirmation_email


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


class TweetViewSet(viewsets.ViewSet):

    def list(self):
        game_id = self.request.query_params.get('game')
        game = Game.objects.filter(game__id=game_id).first()
        tweets = games_manager.create_tweets_by_game_name(game)
        serializer = TweetSerializer(tweets, many=True)

        return Response(serializer.data)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    model = User
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def partial_update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        new_email = request.data.pop('email', None)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if new_email:
            pass

