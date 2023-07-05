from rest_framework import serializers
from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


from .models import Product

class ProductIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id']
