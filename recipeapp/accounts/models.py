from django.contrib.auth.models import AbstractUser
from django.db import models

from django.apps import apps
from sklearn.metrics.pairwise import cosine_similarity
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

    def generate_user_tfidf_vector(self):
        liked_recipe_text = [
            like.recipe.get_combined_text() for like in self.likes.all()  # type: ignore
        ]
        tfidf_vectorizer = TfidfLoaderSingleton.get_instance().tfidf_vectorizer
        user_tfidf_vector = tfidf_vectorizer.transform(liked_recipe_text)
        return user_tfidf_vector

    def get_personalized_feed(self, n=10):
        user_tfidf_vector = self.generate_user_tfidf_vector()
        tfidf_matrix = TfidfLoaderSingleton.get_instance().tfidf_matrix
        similarities = cosine_similarity(user_tfidf_vector, tfidf_matrix)  # type: ignore

        sorted_indices = similarities.argsort()[0][::-1]
        recipes = apps.get_model("recipes", "Recipe")
        recommended_ids = [idx for idx in sorted_indices[:n]]
        recommended_recipes = recipes.objects.filter(id__in=recommended_ids)
        return recommended_recipes
