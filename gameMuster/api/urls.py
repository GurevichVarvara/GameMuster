from django.urls import include, path
from rest_framework import routers
from gameMuster.api.views import GameViewSet, GameDetail, \
    PlatformViewSet, PlatformDetail, \
    GenreViewSet, GenreDetail, \
    ScreenshotViewSet, ScreenshotDetail

router = routers.DefaultRouter()
router.register(r'games', GameViewSet)
router.register(r'platforms', PlatformViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'screenshots', ScreenshotViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('games/<int:pk>', GameDetail.as_view(), name='user-detail'),
    path('platforms/<int:pk>', PlatformDetail.as_view(), name='platform-detail'),
    path('genres/<int:pk>', GenreDetail.as_view(), name='genres-detail'),
    path('screenshots/<int:pk>', ScreenshotDetail.as_view(), name='screenshots-detail'),
]
