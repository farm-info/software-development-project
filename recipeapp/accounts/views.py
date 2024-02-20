from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from .forms import FullUserCreationForm
from django.contrib.auth.decorators import login_required

from .forms import FullUserCreationForm, CustomUserChangeForm
from django.contrib.auth import get_user_model


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
            user = form.save()
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


def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'editprofile.html', {'form': form})
