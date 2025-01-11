from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .forms import AdminProfileForm, FullUserCreationForm
from django.contrib.auth.decorators import login_required


from django.urls import reverse
from .forms import EditProfileForm
from recipes.models import Recipe, Comment


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


def register_view(request):
    if request.method == "POST":
        form = FullUserCreationForm(request.POST)
        if form.is_valid():
            _user = form.save()
            return redirect("home")
    else:
        form = FullUserCreationForm()
    return render(request, "register.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    return redirect("home")


def profile(request):
    return render(request, "profile.html")


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect(reverse("profile"))
        else:
            return HttpResponseBadRequest("Invalid action")

    else:
        form = EditProfileForm(instance=request.user)
        return render(request, "edit_profile.html", {"form": form})


@login_required
def admin_profile(request):
    if request.method == "POST":
        form = AdminProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect(reverse("admin_profile"))
        else:
            return HttpResponseBadRequest("Invalid action")

    else:
        form = AdminProfileForm(instance=request.user)
        return render(request, "admin_profile.html", {"form": form})


def admin_register(request):
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "admin_register":
            form = FullUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect("profile")
        else:
            return redirect("your_previous_page")
    else:
        form = FullUserCreationForm()
    return render(request, "admin_register.html", {"form": form})
