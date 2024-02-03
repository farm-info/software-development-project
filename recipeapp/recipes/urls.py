from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("search/", views.search, name="search"),
    path("recipe/<int:id>/", views.recipe, name="recipe"),
    path("like/", views.like_recipe, name="like_recipe"),
    path("upload/", views.upload_recipe, name="upload_recipe"),
    path("recipe/<int:id>/edit/", views.edit_recipe, name="edit_recipe"),
]
