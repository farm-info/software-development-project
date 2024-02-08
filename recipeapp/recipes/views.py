from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef, Value
from .models import Recipe, Like, Comment
from .forms import RecipeForm
from django.http import HttpResponseBadRequest


def home(request):
    # TODO actual algorithm
    # placeholder
    if request.user.is_authenticated:
        likes = Like.objects.filter(user=request.user, recipe=OuterRef("pk"))
        recipes = Recipe.objects.all().annotate(has_liked=Exists(likes))
    else:
        recipes = Recipe.objects.all().annotate(has_liked=Value(False))
    return render(request, "home.html", {"recipes": recipes})


def search(request):
    # TODO actual algorithm
    # placeholder
    results = Recipe.objects.all()
    return render(request, "search.html", {"results": results})


def recipe(request, id):
    recipe = get_object_or_404(Recipe, pk=id)
    comments = Comment.objects.filter(recipe=recipe, parent_comment_id=None)
    return render(request, "recipe.html", {"recipe": recipe, "comments": comments})


@login_required
def like_recipe(request):
    recipe_id = request.POST.get("recipe_id")
    recipe = Recipe.objects.get(id=recipe_id)
    user = request.user
    like, created = Like.objects.get_or_create(user=user, recipe=recipe)
    if not created:
        like.delete()
    return redirect(request.META.get("HTTP_REFERER", "home"))


@login_required
def add_comment(request):
    author = request.user
    recipe_id = request.POST.get("recipe_id")
    recipe = Recipe.objects.get(id=recipe_id)
    parent_comment_id = request.POST.get("parent_comment_id")
    parent_comment = (
        Comment.objects.get(id=parent_comment_id) if parent_comment_id else None
    )
    text = request.POST["text"]

    comment = Comment(
        author=author, recipe=recipe, parent_comment_id=parent_comment, text=text
    )
    comment.save()
    return redirect(request.META.get("HTTP_REFERER", "home"))


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


@login_required
def edit_recipe(request, id):
    recipe = get_object_or_404(Recipe, pk=id)
    if request.method == "POST":
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            recipe = form.save()
            return redirect("recipe", id=recipe.id)
        else:
            return HttpResponseBadRequest("Invalid action")

    form = RecipeForm(instance=recipe)
    return render(request, "edit_recipe.html", {"form": form, "recipe": recipe})


@login_required
def verify_recipe(request, id, action):
    recipe = get_object_or_404(Recipe, pk=id)
    if action == "verify":
        recipe.is_verified = True
    elif action == "unverify":
        recipe.is_verified = False
    else:
        return HttpResponseBadRequest("Invalid action")
    recipe.save()
    return redirect("recipe", id=id)


@login_required
def delete_recipe(request, id):
    recipe = get_object_or_404(Recipe, pk=id)
    recipe.delete()
    return redirect("home")
