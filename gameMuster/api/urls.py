from django.urls import include, path
from rest_framework import routers
from gameMuster.api.views import GameViewSet, GameDetail, PlatformViewSet, PlatformDetail, GenreViewSet, GenreDetail

router = routers.DefaultRouter()
router.register(r'games', GameViewSet)
router.register(r'platforms', PlatformViewSet)
router.register(r'genres', GenreViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('games/<int:pk>', GameDetail.as_view(), name='user-detail'),
    path('platforms/<int:pk>', PlatformDetail.as_view(), name='platform-detail'),
    path('genres/<int:pk>', GenreDetail.as_view(), name='genres-detail'),
]
