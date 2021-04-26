from django.urls import path
from gameMuster import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:game_id>/', views.detail, name='detail')
]