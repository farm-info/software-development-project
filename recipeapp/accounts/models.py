from django.contrib.auth.models import AbstractUser
from django.db import models

from django.apps import apps
from recipes.tfidf_loader import TfidfLoaderSingleton

from datetime import date


class User(AbstractUser):
    ACCOUNT_TYPE_CHOICES = (
        ("admin", "Admin"),
        ("professional", "Professional"),
        ("user", "User"),
    )

    account_type = models.CharField(
        max_length=12,
        choices=ACCOUNT_TYPE_CHOICES,
        default="user",
    )
    email = models.EmailField(
        unique=True,
        blank=True,
        help_text="Optional but recommended. Used for account recovery.",
    )
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", null=True, blank=True
    )
    date_of_birth = models.DateField(null=True, blank=True)

    def age(self):
        if self.date_of_birth:
            return date.today().year - self.date_of_birth.year
        else:
            return None

    def get_personalized_feed(self, n=10):
        liked_recipe_text = [
            like.recipe.get_combined_text() for like in self.likes.all()  # type: ignore
        ]
        liked_recipe_text = " ".join(liked_recipe_text)
        return TfidfLoaderSingleton.get_instance().search_item(liked_recipe_text, n)  # type: ignore
