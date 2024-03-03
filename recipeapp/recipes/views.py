from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef, Value
from django.http import HttpResponseBadRequest
from .models import Recipe, Like, Comment
from .forms import RecipeForm


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


def recipe(request, recipe_id):
    requested_recipe = get_object_or_404(Recipe, pk=recipe_id)
    comments = Comment.objects.filter(recipe=requested_recipe, parent_comment_id=None)
    return render(
        request, "recipe.html", {"recipe": requested_recipe, "comments": comments}
    )


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
    rating = request.POST["rating"]

    comment = Comment(
        author=author,
        recipe=recipe,
        parent_comment_id=parent_comment,
        text=text,
        rating=rating,
    )
    comment.save()
    return redirect(request.META.get("HTTP_REFERER", "home"))


@login_required
def upload_recipe(request):
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            new_recipe = form.save(commit=False)
            new_recipe.author = request.user
            new_recipe.save()
            return redirect("recipe", id=new_recipe.id)
    else:
        form = RecipeForm()
    return render(request, "upload_recipe.html", {"form": form})


@login_required
def edit_recipe(request, recipe_id):
    editing_recipe = get_object_or_404(Recipe, pk=recipe_id)
    if request.method == "POST":
        form = RecipeForm(request.POST, instance=editing_recipe)
        if form.is_valid():
            editing_recipe = form.save()
            return redirect("recipe", id=editing_recipe.id)
        else:
            return HttpResponseBadRequest("Invalid action")

    form = RecipeForm(instance=editing_recipe)
    return render(request, "edit_recipe.html", {"form": form, "recipe": editing_recipe})


@login_required
def verify_recipe(request, recipe_id, action):
    if request.user.account_type != "professional":
        return HttpResponseBadRequest("Invalid action")
    editing_recipe = get_object_or_404(Recipe, pk=recipe_id)
    if action == "verify":
        editing_recipe.is_verified = True
    elif action == "unverify":
        editing_recipe.is_verified = False
    else:
        return HttpResponseBadRequest("Invalid action")
    editing_recipe.save()
    return redirect("recipe", id=recipe_id)


@login_required
def delete_recipe(request, recipe_id):
    editing_recipe = get_object_or_404(Recipe, pk=recipe_id)
    if editing_recipe.author != request.user:
        return HttpResponseBadRequest("Invalid action")
    editing_recipe.delete()
    return redirect("home")
