"""
Auto Generated serializers.py
Automatically generated with ❤️ by django-sage-painless
"""
from rest_framework.serializers import ModelSerializer

from products.models.category import Category

from products.models.product import Product

from products.models.discount import Discount


class CategorySerializer(ModelSerializer):
    """
    Category Serializer
    Auto generated
    """
    class Meta:
        model = Category
        fields = [
            'id',
            'title',
            'created',
            'modified',
        
        ]


class ProductSerializer(ModelSerializer):
    """
    Product Serializer
    Auto generated
    """
    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'description',
            'price',
            'category',
            'created',
            'modified',
        
        ]


class DiscountSerializer(ModelSerializer):
    """
    Discount Serializer
    Auto generated
    """
    class Meta:
        model = Discount
        fields = [
            'id',
            'product',
            'discount',
            'created',
            'modified',
        
        ]
