import sys
from django.apps import AppConfig, apps
from .tfidf_loader import TfidfLoaderSingleton


class RecipesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "recipes"

    def initialize_tfidf_loader(self):
        try:
            recipe_model = apps.get_model("recipes", "Recipe")
            loader = TfidfLoaderSingleton.get_instance()
            loader.initialize(recipe_model)
            print("TfidfLoader initialized!")
        except Exception as e:
            print(f"Failed to initialize TfidfLoader: {e}")

    def ready(self):
        # TODO kinda janky
        if "migrate" not in sys.argv:
            self.initialize_tfidf_loader()
