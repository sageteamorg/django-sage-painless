"""
Auto Generated test
You may need to change some parts
"""
from django.apps import apps
from rest_framework.test import APITestCase
from django_seed import Seed

from products.models import *

seeder = Seed.seeder()


class ProductsModelTest(APITestCase):
    """
    products Model Test
    Auto Generated
    """

    def setUp(self) -> None:
        self.models = apps.get_app_config('products').get_models()
        self.models_name = [model._meta.object_name for model in self.models]

    def test_category_model(self):
        """
        test Category creation
        """
        seeder.add_entity(Category, 1)
        seeder.execute()  # create instance
        # assertions
        self.assertTrue(Category.objects.exists())
        self.assertIn('Category', self.models_name)

    def test_product_model(self):
        """
        test Product creation
        """
        seeder.add_entity(Product, 1)
        seeder.execute()  # create instance
        # assertions
        self.assertTrue(Product.objects.exists())
        self.assertIn('Product', self.models_name)

    def test_discount_model_signal(self):
        """
        test Product - Discount signal
        """
        seeder.add_entity(Product, 1)
        seeder.execute()  # create instance
        # assertions
        self.assertTrue(Product.objects.exists())
        self.assertTrue(Discount.objects.exists())
        first_object = Product.objects.first()
        second_object = Discount.objects.first()
        self.assertEqual(second_object.product, first_object)
