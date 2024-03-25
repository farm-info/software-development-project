import os
from django.core.management import BaseCommand
from ...models import Recipe


class Command(BaseCommand):
    help = "Remove pictures in media/photos/ that are not used by any recipe"

    def handle(self, *args, **options):
        used_pictures = set()
        for recipe in Recipe.objects.all():
            if recipe.photo:
                photo_name = recipe.photo.name.split("/")[-1]
                used_pictures.add(photo_name)

        media_path = "media/photos/"
        for picture in os.listdir(media_path):
            if picture not in used_pictures:
                os.remove(media_path + picture)
                print(f"Removed {picture}")
