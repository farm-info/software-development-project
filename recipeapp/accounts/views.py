from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(request.META.get("HTTP_REFERER", "home"))
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect(request.META.get("HTTP_REFERER", "home"))
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    return redirect("home")


def profile(request):
    return render(request, "profile.html")
