from django.apps import AppConfig
from .tfidf_loader import TfidfLoaderSingleton


class RecipesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "recipes"

    def ready(self):
        loader = TfidfLoaderSingleton.get_instance()
        loader.initialize()
        print("TfidfLoader initialized!")
