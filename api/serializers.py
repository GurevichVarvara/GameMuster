from rest_framework import serializers

from gameMuster.models import Game, Platform, Genre, Screenshot, FavoriteGame
from users.models import User


class PlatformSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Platform
        fields = '__all__'


class GenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class ScreenshotSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Screenshot
        fields = '__all__'


class GameSerializer(serializers.HyperlinkedModelSerializer):
    platforms = PlatformSerializer(many=True,
                                   required=False)
    genres = GenreSerializer(many=True,
                             required=False)
    screenshot_set = serializers.HyperlinkedRelatedField(
        many=True,
        required=False,
        read_only=True,
        view_name='screenshot-detail'
    )

    class Meta:
        model = Game
        fields = '__all__'
        extra_fields = ['screenshot_set']


class FavoriteGameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FavoriteGame
        fields = '__all__'


class TweetSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=400)
    publisher = serializers.CharField(max_length=200)
    date = serializers.DateTimeField()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username',
                  'email',
                  'birthday',
                  'first_name',
                  'last_name']
