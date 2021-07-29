"""
Auto Generated test
You may need to change some parts
"""
from django.apps import apps
from django.urls import reverse
from rest_framework.test import APITestCase
from django_seed import Seed


from products.models.category import Category

from products.models.product import Product

from products.models.discount import Discount


seeder = Seed.seeder()

class ProductTest(APITestCase):
    """
    Product Test
    Auto Generated
    """
    def setUp(self) -> None:
        self.models = apps.get_app_config('products').get_models()
        self.models_name = [model._meta.object_name for model in self.models]
        
        seeder.add_entity(Category, 3)
        
        seeder.add_entity(Product, 3)
        
        seeder.add_entity(Discount, 3)
        
        seeder.execute()  # create instances
    
    def test_product_model(self):
        """test Product creation"""
        seeder.add_entity(Product, 1)
        seeder.execute()  # create instance
        # assertions
        self.assertTrue(Product.objects.exists())
        self.assertIn('Product', self.models_name)
    
    def test_product_list_success(self):
        """test Product list"""
        url = reverse('product-list')
        response = self.client.get(url)
        # assertions
        self.assertEqual(response.status_code, 200)
        if type(response.data) == dict:
            if response.data.get('count'):
                self.assertGreater(response.data['count'], 0)
        else:
            self.assertGreater(len(response.data), 0)

    def test_product_detail_success(self):
        """test Product detail"""
        product = Product.objects.first()
        url = reverse('product-detail', args=[product.pk])
        response = self.client.get(url)
        # assertions
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(response.data.get('title'), product.title)
        
        self.assertEqual(response.data.get('description'), product.description)
        
        self.assertEqual(response.data.get('price'), product.price)
        
        
        
        
        
        
        
        
    
    
