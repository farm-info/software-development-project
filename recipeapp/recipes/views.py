from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef, Value
from .models import Recipes, Likes, Comments
from .forms import RecipeForm


def home(request):
    # TODO actual algorithm
    # placeholder
    if request.user.is_authenticated:
        likes = Likes.objects.filter(user=request.user, recipe=OuterRef("pk"))
        recipes = Recipes.objects.all().annotate(has_liked=Exists(likes))
    else:
        recipes = Recipes.objects.all().annotate(has_liked=Value(False))
    return render(request, "home.html", {"recipes": recipes})


def search(request):
    # TODO actual algorithm
    # placeholder
    results = Recipes.objects.all()
    return render(request, "search.html", {"results": results})


def recipe(request, id):
    recipe = get_object_or_404(Recipes, pk=id)
    return render(request, "recipe.html", {"recipe": recipe})


@login_required
def like_recipe(request):
    recipe_id = request.POST.get("recipe_id")
    recipe = Recipes.objects.get(id=recipe_id)
    user = request.user
    like, created = Likes.objects.get_or_create(user=user, recipe=recipe)
    if not created:
        like.delete()
    return redirect(request.META.get("HTTP_REFERER", "home"))


# just pasted some ai generated stuff, not sure if it works
@login_required
def add_comment(request, id):
    post = get_object_or_404(Recipes, pk=id)
    if request.method == "POST":
        text = request.POST["comment"]
        comment = Comments(author=request.user, post=post, text=text)
        comment.save()
        return redirect("recipe", id=recipe.id)
    else:
        return render(request, "add_comment.html", {"post": post})


# TODO deal with is_imported_recipen
# TODO test upload recipe
@login_required
def upload_recipe(request):
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            return redirect("recipe", id=recipe.id)
    else:
        form = RecipeForm()
    return render(request, "upload_recipe.html", {"form": form})


# TODO
@login_required
def edit_recipe(request, id):
    recipe = get_object_or_404(Recipes, pk=id)
    if request.method == "POST":
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            recipe = form.save()
            return redirect("recipe", id=recipe.id)
    else:
        form = RecipeForm(instance=recipe)
    return render(request, "edit_recipe.html", {"form": form})
