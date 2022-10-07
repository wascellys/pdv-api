import django
import pytest

django.setup()
import json
from rest_framework import status

from api.tests.conftest import URL, create_product, api_client

pytestmark = pytest.mark.django_db


def test_get_products_200(api_client):
    response = api_client.get(f'{URL}/products/')
    assert response.status_code == status.HTTP_200_OK


def test_retrive_product_200(api_client, create_product):
    response = api_client.get(f'{URL}/products/{create_product.id}/')
    assert response.status_code == status.HTTP_200_OK


def test_retrive_product_404(api_client, create_product):
    response = api_client.get(f'{URL}/products/999/')
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_post_products_201(api_client):
    body = {"name": "HP Externo Seagate", "type": "product", "price": "350", "commission": "6"}
    response = api_client.post(f'{URL}/products/', data=body)
    assert response.status_code == status.HTTP_201_CREATED


def test_post_service_201(api_client):
    body = {"name": "Instalação Windows", "type": "service", "price": "100", "commission": "6"}
    response = api_client.post(f'{URL}/products/', data=body)
    assert response.status_code == status.HTTP_201_CREATED


def test_update_products_200(api_client, create_product):
    body = {"name": "HP Externo Samsung", "type": "product", "price": "350", "commission": "6"}
    response = api_client.put(f'{URL}/products/{create_product.id}/', data=body)
    data = json.loads(response.content)
    assert response.status_code == status.HTTP_200_OK
    assert body.get("name") == data.get("name")


def test_update_services_200(api_client, create_service):
    body = {"name": "Instalação windows", "type": "product", "price": "350", "commission": "6"}
    response = api_client.put(f'{URL}/products/{create_service.id}/', data=body)
    data = json.loads(response.content)
    assert response.status_code == status.HTTP_200_OK
    assert body.get("name") == data.get("name")


def test_delete_products_204(api_client, create_product):
    response = api_client.delete(f'{URL}/products/{create_product.id}/')
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_update_products_not_exists_404(api_client):
    body = {"name": "Case Notebook Apple", "type": "product", "price": "350", "commission": "6"}
    response = api_client.put(f'{URL}/products/9999/', data=body)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_products_not_exists_404(api_client, create_product):
    response = api_client.delete(f'{URL}/products/999/')
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_post_products_type_invalid(api_client):
    body = {"name": "HP Externo Seagate", "type": "produto", "price": "350", "commission": "6"}
    response = api_client.post(f'{URL}/products/', data=body)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
