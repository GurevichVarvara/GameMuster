from rest_framework import serializers

from gameMuster.models import Game, Platform, Genre, Screenshot


class PlatformSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Platform
        fields = '__all__'


class GenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class GameSerializer(serializers.HyperlinkedModelSerializer):
    platforms = PlatformSerializer(many=True,
                                   required=False)
    genres = GenreSerializer(many=True,
                             required=False)

    class Meta:
        model = Game
        fields = '__all__'


class ScreenshotSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Screenshot
        fields = '__all__'
