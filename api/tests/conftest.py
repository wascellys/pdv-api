import json
from rest_framework.test import APIClient
import pytest
import requests
from decouple import config

from api.models import Product, Client, Seller, Sale, OrdersSale

pytestmark = pytest.mark.django_db

URL = f'{config("WEB_HOST")}'


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_seller():
    seller, created = Seller.objects.get_or_create(name="Morais Seller")
    return seller


@pytest.fixture
def create_client():
    client, created = Client.objects.get_or_create(name="Ferreira Client")
    return client


@pytest.fixture
def create_product():
    product, created = Product.objects.get_or_create(name="Impressora HP", price="350", commission="5", type="product")
    return product


@pytest.fixture
def create_sale(create_client, create_seller):
    sale, created = Sale.objects.get_or_create(client=create_client, seller=create_seller)
    return sale


@pytest.fixture
def create_service():
    product, created = Product.objects.get_or_create(name="Impressora HP", price="350", commission="5", type="product")
    return product

@pytest.fixture
def create_order(create_sale, create_product):
    order, created = OrdersSale.objects.get_or_create(product=create_product, sale=create_sale)
    return order