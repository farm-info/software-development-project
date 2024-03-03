from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


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
    ingredients = models.TextField()
    steps = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def get_ingredients_lines(self):
        return self.ingredients.splitlines() if self.ingredients else []

    def get_steps_lines(self):
        return self.steps.splitlines() if self.steps else []

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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="likes")
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            "user",
            "recipe",
        )


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


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    comment = models.ForeignKey(
        Comment, null=True, on_delete=models.CASCADE, related_name="notif_comment"
    )
    like = models.ForeignKey(Like, null=True, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(comment__isnull=False, like__isnull=True)
                | models.Q(comment__isnull=True, like__isnull=False),
                name="comment_xor_like",
            ),
        ]
