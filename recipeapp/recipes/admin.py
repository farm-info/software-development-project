from django.contrib import admin
from .models import Recipe, Like, Comment


@admin.register(Recipe)
class RecipesAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "is_imported_recipe", "is_verified")
    list_filter = ("is_imported_recipe", "is_verified")
    search_fields = ("title", "description", "author__username")


@admin.register(Like)
class LikesAdmin(admin.ModelAdmin):
    list_display = ("user", "recipe", "created_date")
    list_filter = ("created_date",)
    search_fields = ("user__username", "recipe__title")


@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ("author", "recipe", "text", "created_date", "parent_comment_id")
    list_filter = ("created_date",)
    search_fields = ("author__username", "recipe__title")
