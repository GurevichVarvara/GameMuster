from django.urls import include, path
from rest_framework import routers
from gameMuster.api.views import GameViewSet, GameDetail, \
    PlatformViewSet, PlatformDetail, \
    GenreViewSet, GenreDetail, \
    ScreenshotViewSet, ScreenshotDetail, \
    FavoriteGameViewSet, FavoriteGameDetail

router = routers.DefaultRouter()
router.register(r'games', GameViewSet)
router.register(r'platforms', PlatformViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'screenshots', ScreenshotViewSet, basename='Screenshot')
router.register(r'favorite_games', FavoriteGameViewSet, basename='FavoriteGame')

urlpatterns = [
    path('', include(router.urls)),
    path('games/<int:pk>', GameDetail.as_view(), name='user-detail'),
    path('platforms/<int:pk>', PlatformDetail.as_view(), name='platform-detail'),
    path('genres/<int:pk>', GenreDetail.as_view(), name='genre-detail'),
    path('screenshots/<int:pk>', ScreenshotDetail.as_view(), name='screenshot-detail'),
    path('favorite_games/<int:pk>', FavoriteGameDetail.as_view(), name='favorite_game-detail'),
]
