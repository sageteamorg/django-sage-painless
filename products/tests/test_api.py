"""
Auto Generated test
You may need to change some parts
"""
from django.urls import reverse
from rest_framework.test import APITestCase
from django_seed import Seed

from products.models import *

seeder = Seed.seeder()


class ProductsAPITest(APITestCase):
    """
    products API Test
    Auto Generated
    """

    def setUp(self) -> None:

        seeder.add_entity(Category, 3)

        seeder.add_entity(Product, 3)

        seeder.execute()  # create instances

    def test_category_list_success(self):
        """
        test Category list
        """
        url = reverse('category-list')
        response = self.client.get(url)
        # assertions
        self.assertEqual(response.status_code, 200)
        if isinstance(response.data, dict):
            if response.data.get('count'):
                self.assertGreater(response.data['count'], 0)
        else:
            self.assertGreater(len(response.data), 0)

    def test_category_detail_success(self):
        """
        test Category detail
        """
        category = Category.objects.first()
        url = reverse('category-detail', args=[category.pk])
        response = self.client.get(url)
        # assertions
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data.get('title'), category.title)

    def test_product_list_success(self):
        """
        test Product list
        """
        url = reverse('product-list')
        response = self.client.get(url)
        # assertions
        self.assertEqual(response.status_code, 200)
        if isinstance(response.data, dict):
            if response.data.get('count'):
                self.assertGreater(response.data['count'], 0)
        else:
            self.assertGreater(len(response.data), 0)

    def test_product_detail_success(self):
        """
        test Product detail
        """
        product = Product.objects.first()
        url = reverse('product-detail', args=[product.pk])
        response = self.client.get(url)
        # assertions
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data.get('title'), product.title)

        self.assertEqual(response.data.get('description'), product.description)

        self.assertEqual(response.data.get('price'), product.price)

    def test_discount_list_success(self):
        """
        test Discount list
        """
        url = reverse('discount-list')
        response = self.client.get(url)
        # assertions
        self.assertEqual(response.status_code, 200)
        if isinstance(response.data, dict):
            if response.data.get('count'):
                self.assertGreater(response.data['count'], 0)
        else:
            self.assertGreater(len(response.data), 0)

    def test_discount_detail_success(self):
        """
        test Discount detail
        """
        discount = Discount.objects.first()
        url = reverse('discount-detail', args=[discount.pk])
        response = self.client.get(url)
        # assertions
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data.get('discount'), discount.discount)
