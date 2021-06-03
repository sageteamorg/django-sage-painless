"""
Auto Generated serializers.py
You may need to change some parts
"""
from rest_framework.serializers import ModelSerializer

from products.models import *


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'title',
            'created',
            'modified',

        ]


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'title',
            'description',
            'price',
            'category',
            'created',
            'modified',

        ]


class DiscountSerializer(ModelSerializer):
    class Meta:
        model = Discount
        fields = [
            'product',
            'discount',
            'created',
            'modified',

        ]
