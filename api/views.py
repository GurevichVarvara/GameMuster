from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.decorators import permission_classes, api_view, action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

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

    @action(detail=True, methods=['get'])
    def tweets(self, request, pk):
        game = Game.objects.filter(id=pk).first()
        tweets = games_manager.create_tweets_by_game_name(game)
        serializer = TweetSerializer(tweets, many=True)

        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def screenshots(self, request, pk):
        screenshots = Screenshot.objects.filter(game__id=pk)
        serializer = ScreenshotSerializer(screenshots,
                                          context={'request': request},
                                          many=True)

        return Response(serializer.data)


class PlatformViewSet(viewsets.ModelViewSet):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ScreenshotViewSet(viewsets.ModelViewSet):
    queryset = Screenshot.objects.all()
    serializer_class = ScreenshotSerializer


class FavoriteGameViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteGameSerializer

    def get_queryset(self):
        return FavoriteGame.objects.filter(user=self.request.user)


def is_email_valid(email):
    try:
        validate_email(email)
        return not (User.objects.filter(email=email).first() or
                    User.objects.filter(unconfirmed_email=email).first())
    except ValidationError:
        return False


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = User.objects.all()
        else:
            user_id = self.request.user.id
            queryset = User.objects.filter(id=user_id)

        return queryset

    def update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        new_email = request.data.pop('email', None)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if new_email and new_email.lower() != self.request.user.email.lower():
            if is_email_valid(new_email):
                user = request.user
                user.unconfirmed_email = new_email
                user.save()

                send_confirmation_email(self.request, self.request.user, new_email)

                return render(request, 'users/message.html',
                              {'message': 'Please confirm your '
                                          'new email address'})
            else:
                return Response({'Errors': 'Incorrect new email', **serializer.data})

        return Response(serializer.data)

