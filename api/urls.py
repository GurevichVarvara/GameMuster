from django.urls import include, path
from rest_framework import routers
from api.views import GameViewSet, \
    PlatformViewSet, GenreViewSet, \
    ScreenshotViewSet, FavoriteGameViewSet, \
    UserDetail, \
    change_user_password, UserViewSet, BaseUserDetail

router = routers.DefaultRouter()
router.register(r'games', GameViewSet)
router.register(r'platforms', PlatformViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'screenshots', ScreenshotViewSet, basename='screenshot')
router.register(r'favorite', FavoriteGameViewSet, basename='favoritegame')
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('users/<int:pk>',
         BaseUserDetail.as_view(),
         name='admin-user-detail'),
    path('user',
         UserDetail.as_view(),
         name='user-detail'),
    path('change_password',
         change_user_password,
         name='change_user_password')
]