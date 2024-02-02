from django.db import models
from django.contrib.auth.models import User


class Recipes(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    is_imported_recipe = models.BooleanField(default=False)
    photo = models.ImageField(upload_to="media/photos/", null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    ingredients = models.TextField()
    steps = models.TextField()

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(
                        is_imported_recipe=True,
                        description__isnull=False,
                        ingredients__isnull=False,
                    )
                    | models.Q(is_imported_recipe=False)
                ),
                name="imported_recipe_requires_description_ingredients",
            ),
        ]
