from django.shortcuts import render
from .models import Recipes


def home(request):
    recipes = Recipes.objects.all()
    return render(request, "home.html", {"posts": recipes})


def search(request):
    return render(request, "search.html")
