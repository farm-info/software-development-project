from django.core.management import BaseCommand
from recipes.tfidf_loader import TfidfLoaderSingleton


class Command(BaseCommand):
    help = "Reprocess all recipes for the recommendation system"

    def handle(self, *args, **options):
        print("Reprocessing... ", end="")
        TfidfLoaderSingleton.get_instance().reprocess()
        print("done")
