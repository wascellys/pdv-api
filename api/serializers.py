from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from api.models import Client, Seller, Sale, Product, Person, OrdersSale


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class PersonSerializer(ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'name']
        abstract = True


class SellerSerializer(ModelSerializer):
    class Meta:
        model = Seller
        fields = "__all__"


class ClientSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"


class SaleSerializer(ModelSerializer):
    class Meta:
        model = Sale
        fields = "__all__"


class OrdersSaleSerializer(ModelSerializer):
    product_name = SerializerMethodField(read_only=True)

    def get_product_name(self, obj):
        return obj.product.name

    class Meta:
        model = OrdersSale
        fields = ['id', 'sale', 'product', 'product_name']
