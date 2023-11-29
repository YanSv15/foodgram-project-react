import csv
import os

from django.core.management.base import BaseCommand
from django.conf import settings

from posts.models import Ingredient


def get_reader(file_name: str):
    csv_path = os.path.join(settings.BASE_DIR, 'static/data/', file_name)
    csv_file = open(csv_path, 'r', encoding='utf-8')
    reader = csv.reader(csv_file, delimiter=',')
    return reader


class Command(BaseCommand):
    def handle(self, *args, **options):
        csv_reader = get_reader('ingredients.csv')
        for row in csv_reader:
            obj, created = Ingredient.objects.get_or_create(
                name=row[0],
                measurement_unit=row[1]
            )
        print('ingredients - OK')
