from django.urls import include, path
from rest_framework import routers
from gameMuster.api import views

router = routers.DefaultRouter()
router.register(r'games', views.GameViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
