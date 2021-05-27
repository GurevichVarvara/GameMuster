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


class BaseViewSet(viewsets.ModelViewSet):

    def retrieve(self, request, pk):
        target_object = self.queryset.filter(id=pk).first()

        return Response(self.serializer_class(target_object,
                                              context={'request': request}).data)


class GameViewSet(BaseViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    @action(detail=True, methods=['get'])
    def tweets(self, request, pk):
        game = Game.objects.filter(id=pk).first()
        tweets = games_manager.create_tweets_by_game_name(game)
        serializer = TweetSerializer(tweets, many=True)

        return Response(serializer.data)


class PlatformViewSet(BaseViewSet):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer


class GenreViewSet(BaseViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ScreenshotViewSet(viewsets.ModelViewSet):
    serializer_class = ScreenshotSerializer

    def get_queryset(self, game_id=None):
        return Screenshot.objects.filter(game__id=game_id) \
            if game_id else Screenshot.objects.all()

    def list(self, request, target):
        queryset = self.get_queryset(target)

        return Response(self.serializer_class(queryset,
                                              context={'request': request},
                                              many=True).data)

    def retrieve(self, request, pk):
        target_object = self.get_queryset().filter(id=pk).first()

        return Response(self.serializer_class(target_object,
                                              context={'request': request}).data)


class FavoriteGameViewSet(BaseViewSet):
    serializer_class = FavoriteGameSerializer

    def get_queryset(self):
        return FavoriteGame.objects.filter(user=self.request.user)


class TweetViewSet(viewsets.ViewSet):
    serializer_class = TweetSerializer

    def list(self, request, target):
        game = Game.objects.filter(id=target).first()
        tweets = games_manager.create_tweets_by_game_name(game)
        serializer = self.serializer_class(tweets, many=True)

        return Response(serializer.data)


def is_email_valid(email):
    try:
        validate_email(email)
        return not (User.objects.filter(email=email).first() or
                    User.objects.filter(unconfirmed_email=email).first())
    except ValidationError:
        return False


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class BaseUserDetail(generics.RetrieveUpdateDestroyAPIView):
    model = User
    serializer_class = UserSerializer

    def partial_update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        new_email = request.data.pop('email', None)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if new_email != self.request.user.email:
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


class UserDetail(BaseUserDetail):

    def get_object(self):
        return self.request.user


@api_view(['GET'])
@permission_classes([])
def change_user_password(request):
    return redirect('password_reset')
