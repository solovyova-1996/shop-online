import json, os

from django.core.management import BaseCommand

from mainapp.models import Category, Product

JSON_PATH = 'mainapp/fixtures'


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r',
              encoding='windows-1251') as f:
        return json.load(f)


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = load_from_json('categories')
        Category.objects.all().delete()
        for category in categories:
            cat = category.get('fields')
            cat['id'] = category.get('pk')
            new_category = Category(**cat)
            new_category.save()

        products = load_from_json('products')
        Product.objects.all().delete()
        for product in products:
            prod = product.get('fields')
            category = prod.get('category')
            _category = Category.objects.get(id=category)
            prod['category'] = _category
            new_prod = Product(**prod)
            new_prod.save()
