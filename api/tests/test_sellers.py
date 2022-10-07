import django

django.setup()
import json
import pytest
from rest_framework import status
from api.tests.conftest import URL, create_seller, api_client

pytestmark = pytest.mark.django_db


def test_get_sellers_200(api_client):
    response = api_client.get(f'{URL}/sellers/')
    assert response.status_code == status.HTTP_200_OK


def test_retrive_seller_200(api_client, create_seller):
    response = api_client.get(f'{URL}/sellers/{create_seller.id}/')
    assert response.status_code == status.HTTP_200_OK

def test_retrive_seller_404(api_client):
    response = api_client.get(f'{URL}/sellers/154/')
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_post_sellers_201(api_client):
    body = {"name": "Morais Test"}
    response = api_client.post(f'{URL}/sellers/', data=body)
    assert response.status_code == status.HTTP_201_CREATED


def test_update_sellers_200(api_client, create_seller):
    body = {"name": "Morais Test"}
    response = api_client.put(f'{URL}/sellers/{create_seller.id}/', data=body)
    data = json.loads(response.content)
    assert response.status_code == status.HTTP_200_OK
    assert data.get("name") == body.get("name")


def test_delete_sellers_204(api_client, create_seller):
    response = api_client.delete(f'{URL}/sellers/{create_seller.id}/')
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_update_sellers_not_exists_404(api_client):
    body = {"name": "Morais Test"}
    response = api_client.put(f'{URL}/sellers/9999/', data=body)
    data = json.loads(response.content)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_sellers_not_exists_404(api_client, create_seller):
    response = api_client.delete(f'{URL}/sellers/999/')
    assert response.status_code == status.HTTP_404_NOT_FOUND
