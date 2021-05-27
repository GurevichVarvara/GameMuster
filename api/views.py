from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.decorators import permission_classes, api_view, action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.http import Http404

from gameMuster.models import Game, Platform, Genre, Screenshot, FavoriteGame
from api.serializers import GameSerializer, PlatformSerializer, \
    GenreSerializer, ScreenshotSerializer, FavoriteGameSerializer, \
    TweetSerializer, UserSerializer
from gameMuster.game_managers.games_manager import games_manager
from users.models import User
from users.views import send_confirmation_email


class BaseViewSet(viewsets.ModelViewSet):

    def retrieve(self, request, pk):
        current_object = get_object_or_404(self.queryset,
                                           pk=pk)
        return Response(self.serializer_class(current_object,
                                              context={'request': request}).data)


class GameViewSet(BaseViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class PlatformViewSet(BaseViewSet):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer


class GenreViewSet(BaseViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ScreenshotViewSet(viewsets.ModelViewSet):
    serializer_class = ScreenshotSerializer

    def get_queryset(self):
        queryset = Screenshot.objects.all()
        game = self.request.query_params.get('game')

        if game:
            queryset = queryset.filter(game__id=game)

        return queryset


class FavoriteGameViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteGameSerializer

    def get_queryset(self):
        return FavoriteGame.objects.filter(user=self.request.user)

    def retrieve(self, request, pk):
        game = self.get_queryset().filter(game__id=pk)

        if not game:
            raise Http404('No matching favorite game')

        return Response(self.serializer_class(game,
                                              context={'request': request}).data)


class TweetViewSet(viewsets.ViewSet):

    def list(self):
        game_id = self.request.query_params.get('game')
        game = Game.objects.filter(game__id=game_id).first()
        tweets = games_manager.create_tweets_by_game_name(game)
        serializer = TweetSerializer(tweets, many=True)

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
