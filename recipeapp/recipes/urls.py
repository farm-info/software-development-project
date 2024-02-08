from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("search/", views.search, name="search"),
    path("recipe/<int:id>/", views.recipe, name="recipe"),
    path("like/", views.like_recipe, name="like_recipe"),
    path("add_comment/", views.add_comment, name="add_comment"),
    path("upload/", views.upload_recipe, name="upload_recipe"),
    path("recipe/<int:id>/edit/", views.edit_recipe, name="edit_recipe"),
    path("recipe/<int:id>/delete/", views.delete_recipe, name="delete_recipe"),
]
