from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Product,Order

class Order_api(ModelSerializer):
    class Meta:
        model=Order
        fields="__all__"

class Product_api(ModelSerializer):
    class Meta:
        model=Product
        fields="__all__"

