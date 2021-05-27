from django.urls import include, path
from rest_framework import routers
from api.views import GameViewSet, \
    PlatformViewSet, GenreViewSet, \
    ScreenshotViewSet, FavoriteGameViewSet, \
    TweetViewSet, UserDetail, \
    change_user_password, UserViewSet, BaseUserDetail

router = routers.DefaultRouter()
router.register(r'games', GameViewSet)
router.register(r'platforms', PlatformViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'favorite', FavoriteGameViewSet, basename='favorite')
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/',
         include('rest_framework.urls', namespace='rest_framework')),
    path('games/<int:target>/screenshots',
         ScreenshotViewSet.as_view({'get': 'list'}),
         name='screenshot'),
    path('screenshots/<int:pk>',
         ScreenshotViewSet.as_view({'get': 'retrieve'}),
         name='screenshot-detail'),
    path('games/<int:target>/tweets',
         TweetViewSet.as_view({'get': 'list'}),
         name='tweets'),
    path('favorite/<int:pk>',
         FavoriteGameViewSet.as_view({'get': 'retrieve'}),
         name='favorite-detail'),
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