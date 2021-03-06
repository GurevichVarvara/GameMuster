"""gameMuster URL Configuration"""
from django.urls import path
from gameMuster import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:game_id>/", views.detail, name="detail"),
    path("favorite", views.favorite, name="favorite"),
    path(
        "<int:game_id>/add_to_favorite", views.add_to_favorite, name="add_to_favorite"
    ),
    path(
        "<int:game_id>/remove_from_favorite",
        views.remove_from_favorite,
        name="remove_from_favorite",
    ),
]
