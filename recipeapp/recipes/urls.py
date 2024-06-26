from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("search/", views.search, name="search"),
    path("recipe/<int:recipe_id>/", views.recipe, name="recipe"),
    path("like/", views.like_recipe, name="like_recipe"),
    path("add_comment/", views.add_comment, name="add_comment"),
    path("notifications/", views.notifications, name="notifications"),
    path(
        "notifications/mark_read/",
        views.mark_notifications_read,
        name="mark_notifications_read",
    ),
    path("upload/", views.upload_recipe, name="upload_recipe"),
    path("recipe/<int:recipe_id>/edit/", views.edit_recipe, name="edit_recipe"),
    path("recipe/<int:recipe_id>/delete/", views.delete_recipe, name="delete_recipe"),
    path(
        "recipe/<int:recipe_id>/<str:action>/",
        views.verify_recipe,
        name="verify_recipe",
    ),
    path("about/", views.about, name="about"),
]
