from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email")
    search_fields = ("username", "email", "bio")
    list_filter = ("is_staff", "is_superuser", "date_joined")
