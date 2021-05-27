from django.urls import include, path
from rest_framework import routers
from api.views import GameViewSet, \
    PlatformViewSet, \
    GenreViewSet, \
    ScreenshotViewSet, \
    FavoriteGameViewSet, \
    TweetViewSet, UserDetail, \
    change_user_password, UserViewSet, BaseUserDetail

router = routers.DefaultRouter()
router.register(r'games', GameViewSet)
router.register(r'platforms', PlatformViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'screenshots', ScreenshotViewSet, basename='screenshot')
router.register(r'favorite', FavoriteGameViewSet, basename='favorite')
router.register(r'tweets', TweetViewSet, basename='tweet')
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('games/<int:pk>', GameViewSet.as_view({'get': 'retrieve'}), name='game-detail'),
    path('platforms/<int:pk>', PlatformViewSet.as_view({'get': 'retrieve'}), name='platform-detail'),
    path('genres/<int:pk>', GenreViewSet.as_view({'get': 'retrieve'}), name='genre-detail'),
    path('screenshots/<int:pk>', ScreenshotViewSet.as_view({'get': 'retrieve'}), name='screenshot-detail'),
    path('favorite/<int:pk>', FavoriteGameViewSet.as_view({'get': 'retrieve'}), name='favorite-detail'),
    path('users/<int:pk>', BaseUserDetail.as_view(), name='admin-user-detail'),
    path('user', UserDetail.as_view(), name='user-detail'),
    path('change_password', change_user_password, name='change_user_password')
]