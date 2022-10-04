import json
import pytest
from rest_framework import status

from api.tests.conftest import URL, api_client, create_client, create_product, create_seller, create_service

pytestmark = pytest.mark.django_db


def test_get_sales_200(api_client):
    response = api_client.get(f'{URL}/sales/')
    assert response.status_code == status.HTTP_200_OK


def test_retrive_sale_200(api_client, create_sale):
    response = api_client.get(f'{URL}/sales/{create_sale.id}/')
    assert response.status_code == status.HTTP_200_OK


def test_retrive_sale_404(api_client):
    response = api_client.get(f'{URL}/sales/6985/')
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_post_sales_201(api_client, create_client, create_seller, create_product):
    body = {"client": create_client.id, "seller": create_seller.id,
            "orders": [[create_product.id, 8]]}
    response = api_client.post(f'{URL}/sales/', data=body, format='json')
    assert response.status_code == status.HTTP_201_CREATED


def test_get_orders_sale(api_client, create_sale):
    response = api_client.get(f'{URL}/sales/{create_sale.id}/orders/', format='json')
    assert response.status_code == status.HTTP_200_OK


def test_update_sales_200(api_client, create_client, create_seller, create_product, create_sale):
    body = {"client": create_client.id, "seller": create_seller.id}
    response = api_client.put(f'{URL}/sales/{create_sale.id}/', data=body, format='json')
    assert response.status_code == status.HTTP_200_OK


def test_update_sales_404(api_client, create_client, create_seller, create_product, create_sale):
    body = {"client": create_client.id, "seller": create_seller.id}
    response = api_client.put(f'{URL}/sales/700/', data=body, format='json')
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_sales_400(api_client, create_client, create_seller, create_product, create_sale):
    body = {"clients": create_client.id, "sellers": create_seller.id}
    response = api_client.put(f'{URL}/sales/{create_sale.id}/', data=body, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_delete_sales_204(api_client, create_sale):
    response = api_client.delete(f'{URL}/sales/{create_sale.id}/')
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_sales_not_exists_404(api_client):
    response = api_client.delete(f'{URL}/sales/999/')
    assert response.status_code == status.HTTP_404_NOT_FOUND
