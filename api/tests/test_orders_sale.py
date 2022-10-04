import django
import pytest

django.setup()
import json
from rest_framework import status

from api.tests.conftest import URL, api_client

pytestmark = pytest.mark.django_db


def test_get_orders_200(api_client):
    response = api_client.get(f'{URL}/orders/')
    assert response.status_code == status.HTTP_200_OK


def test_retrive_orders_200(api_client, create_order):
    response = api_client.get(f'{URL}/orders/{create_order.id}/')
    assert response.status_code == status.HTTP_200_OK


def test_retrive_orders_404(api_client):
    response = api_client.get(f'{URL}/orders/9721/')
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_post_orders_201(api_client, create_sale, create_product):
    body = {"sale": create_sale.id, "product": create_product.id}
    response = api_client.post(f'{URL}/orders/', data=body)
    assert response.status_code == status.HTTP_201_CREATED


def test_update_orders_200(api_client, create_order, create_product, create_sale):
    body = {"product": create_product.id, "sale": create_sale.id}
    response = api_client.put(f'{URL}/orders/{create_order.id}/', data=body)
    data = json.loads(response.content)
    assert response.status_code == status.HTTP_200_OK


def test_delete_orders_204(api_client, create_order):
    response = api_client.delete(f'{URL}/orders/{create_order.id}/')
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_update_orders_not_exists_404(api_client):
    body = {"name": "Case Notebook Apple", "type": "order", "price": "350", "commission": "6"}
    response = api_client.put(f'{URL}/orders/9999/', data=body)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_orders_not_exists_404(api_client, create_order):
    response = api_client.delete(f'{URL}/orders/999/')
    assert response.status_code == status.HTTP_404_NOT_FOUND
