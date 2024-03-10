from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef, Value, Q
from django.http import HttpResponseBadRequest
from sklearn.metrics.pairwise import cosine_similarity
from .tfidf_loader import TfidfLoaderSingleton
from .models import Recipe, Like, Comment
from .forms import RecipeForm

tfidf_loader = TfidfLoaderSingleton.get_instance()


def home(request):
    user = request.user
    if user.is_authenticated:
        likes = Like.objects.filter(user=user)
        if likes.exists():
            likes = Like.objects.filter(user=user, recipe=OuterRef("pk"))
            recipes = user.get_personalized_feed().annotate(has_liked=Exists(likes))
            return render(request, "home.html", {"recipes": recipes})

    recipes = Recipe.objects.all().order_by("?").annotate(has_liked=Value(False))
    return render(request, "home.html", {"recipes": recipes})


def search(request):
    query = request.GET.get("query")
    if not query:
        return redirect("home")

    results = tfidf_loader.search_item(query)
    return render(request, "search.html", {"recipes": results, "query": query})


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
    text = request.POST.get("text")
    rating = request.POST.get("rating")
    if not rating:
        rating = None

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
            return redirect("recipe", recipe_id=new_recipe.id)
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
            return redirect("recipe", recipe_id=editing_recipe.id)
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
    return redirect("recipe", recipe_id=recipe_id)


@login_required
def delete_recipe(request, recipe_id):
    editing_recipe = get_object_or_404(Recipe, pk=recipe_id)
    if editing_recipe.author != request.user:
        return HttpResponseBadRequest("Invalid action")
    editing_recipe.delete()
    return redirect("home")


@login_required
def notifications(request):
    # WONTFIX unoptimized code
    notifications = request.user.notifications.filter(is_read=False)
    notifications = notifications.filter(
        Q(comment__recipe__author=request.user) | Q(like__recipe__author=request.user)
    )
    return render(request, "notifications.html", {"notifications": notifications})


@login_required
def mark_notifications_read(request):
    request.user.notifications.update(is_read=True)
    return redirect("notifications")
