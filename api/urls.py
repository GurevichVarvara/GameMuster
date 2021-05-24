from django.urls import include, path
from rest_framework import routers
from api.views import GameViewSet, GameDetail, \
    PlatformViewSet, PlatformDetail, \
    GenreViewSet, GenreDetail, \
    ScreenshotViewSet, ScreenshotDetail, \
    FavoriteGameViewSet, FavoriteGameDetail, \
    TweetViewSet, UserDetail, \
    change_user_password, UserViewSet, BaseUserDetail

router = routers.DefaultRouter()
router.register(r'games', GameViewSet)
router.register(r'platforms', PlatformViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'screenshots', ScreenshotViewSet, basename='Screenshot')
router.register(r'favorite_games', FavoriteGameViewSet, basename='FavoriteGame')
router.register(r'tweets', TweetViewSet, basename='Tweet')
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('games/<int:pk>', GameDetail.as_view(), name='game-detail'),
    path('platforms/<int:pk>', PlatformDetail.as_view(), name='platform-detail'),
    path('genres/<int:pk>', GenreDetail.as_view(), name='genre-detail'),
    path('screenshots/<int:pk>', ScreenshotDetail.as_view(), name='screenshot-detail'),
    path('favorite_games/<int:pk>', FavoriteGameDetail.as_view(), name='favoritegame-detail'),
    path('users/<int:pk>', BaseUserDetail.as_view(), name='admin-user-detail'),
    path('user', UserDetail.as_view(), name='user-detail'),
    path('change_password', change_user_password, name='change_user_password')
]