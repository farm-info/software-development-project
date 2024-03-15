import pandas as pd
import ast
from django.core.management import BaseCommand
from ...models import Recipe


# this only works on a specific csv file, so please modify for other datasets
class Command(BaseCommand):
    help = "Load a csv file into the database"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str)
        parser.add_argument("sample_count", type=int)

    def handle(self, *args, **options):
        data = pd.read_csv(options["csv_file"]).sample(options["sample_count"])
        for _index, row in data.iterrows():
            ingredients = ast.literal_eval(row["Ingredients"])
            ingredients = "\n".join(ingredients)
            _, _created = Recipe.objects.get_or_create(
                title=row["Title"],
                is_imported_recipe=True,
                ingredients=ingredients,
                steps=row["Instructions"],
                # description=row["description"],
                # time_minutes=row["time_minutes"],
                photo="photos/" + row["Image_Name"] + ".jpg",
            )
