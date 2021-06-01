from django.urls import include, path
from rest_framework import routers
from api.views import GameViewSet, \
    PlatformViewSet, GenreViewSet, \
    ScreenshotViewSet, FavoriteGameViewSet, \
    UserViewSet

router = routers.DefaultRouter()
router.register(r'games', GameViewSet)
router.register(r'platforms', PlatformViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'screenshots', ScreenshotViewSet, basename='screenshot')
router.register(r'favorite', FavoriteGameViewSet, basename='favoritegame')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]