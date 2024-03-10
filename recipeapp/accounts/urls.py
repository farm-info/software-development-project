from django.urls import path
from .views import admin_register
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    # path("admin/profile/", views.admin_profile, name="admin_profile"),
    path('admin_register/', admin_register, name='admin_register'),
]
