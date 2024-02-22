from django.urls import path, include
from . import views
from django.contrib import admin


urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("admin/profile/", views.admin_profile, name="admin_profile"),
    path('admin/', admin.site.urls),
    path('', include('recipeapp.urls'))

]
