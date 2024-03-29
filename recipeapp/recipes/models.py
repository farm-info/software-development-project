from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

from .tfidf_loader import TfidfLoaderSingleton


User = settings.AUTH_USER_MODEL


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    is_imported_recipe = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    photo = models.ImageField(upload_to="photos/", null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    time_minutes = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name="Time to cook",
        help_text="in minutes",
    )
    ingredients = models.TextField(help_text="One ingredient per line")
    steps = models.TextField(help_text="One step per line")
    created_date = models.DateTimeField(auto_now_add=True)

    # getters
    def get_ingredients_lines(self):
        return self.ingredients.splitlines() if self.ingredients else []

    def get_steps_lines(self):
        return self.steps.splitlines() if self.steps else []

    def get_combined_text(self) -> str:
        return " ".join(
            [
                str(field)
                for field in [
                    self.title,
                    self.description,
                    self.ingredients,
                    self.steps,
                ]
                if field is not None
            ]
        )

    # recommendation system
    def save(self, *args, **kwargs):
        # retrains the entire database. not ideal, but the best we can do for now
        TfidfLoaderSingleton.get_instance().reprocess()
        return super().save(*args, **kwargs)

    # TODO test
    # TODO filter out liked recipes
    def recommend_similar_recipes(self, n: int = 10) -> "models.QuerySet[Recipe]":
        recipe_text = self.get_combined_text()
        return TfidfLoaderSingleton.get_instance().search_item(recipe_text, n)

    # constrains
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(
                        is_imported_recipe=True,
                        author__isnull=True,
                    )
                    | models.Q(is_imported_recipe=False)
                ),
                name="user_created_recipe_requires_author",
            ),
        ]


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="likes")
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            "user",
            "recipe",
        )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        Notification.objects.create(user=self.user, like=self)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField()
    rating = models.PositiveSmallIntegerField(
        null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_date = models.DateTimeField(auto_now_add=True)
    parent_comment_id = models.ForeignKey(
        "self", null=True, on_delete=models.CASCADE, related_name="replies"
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        Notification.objects.create(user=self.author, comment=self)


class Notification(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications"
    )
    created_date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    comment = models.ForeignKey(Comment, null=True, on_delete=models.CASCADE)
    like = models.ForeignKey(Like, null=True, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(comment__isnull=False, like__isnull=True)
                | models.Q(comment__isnull=True, like__isnull=False),
                name="comment_xor_like",
            ),
        ]
