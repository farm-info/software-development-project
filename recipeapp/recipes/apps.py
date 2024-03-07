from django.apps import AppConfig, apps
from .tfidf_loader import TfidfLoaderSingleton


class RecipesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "recipes"

    def ready(self):
        loader = TfidfLoaderSingleton.get_instance()
        recipe_model = apps.get_model("recipes", "Recipe")
        loader.initialize(recipe_model)
        print("TfidfLoader initialized!")
