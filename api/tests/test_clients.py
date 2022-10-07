import django

django.setup()
import json
import pytest
from rest_framework import status
from api.tests.conftest import URL, create_client, api_client

pytestmark = pytest.mark.django_db


def test_get_clients_200(api_client):
    response = api_client.get(f'{URL}/clients/')
    assert response.status_code == status.HTTP_200_OK


def test_retrive_client_200(api_client, create_client):
    response = api_client.get(f'{URL}/clients/{create_client.id}/')
    assert response.status_code == status.HTTP_200_OK


def test_retrive_client_404(api_client):
    response = api_client.get(f'{URL}/clients/9999/')
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_post_clients_201(api_client):
    body = {"name": "Morais Test"}
    response = api_client.post(f'{URL}/clients/', data=body)
    assert response.status_code == status.HTTP_201_CREATED


def test_update_clients_200(api_client, create_client):
    body = {"name": "Morais Test"}
    response = api_client.put(f'{URL}/clients/{create_client.id}/', data=body)
    data = json.loads(response.content)
    assert response.status_code == status.HTTP_200_OK


def test_delete_clients_204(api_client, create_client):
    response = api_client.delete(f'{URL}/clients/{create_client.id}/')
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_update_clients_not_exists_404(api_client):
    body = {"name": "Morais Test"}
    response = api_client.put(f'{URL}/clients/9999/', data=body)
    data = json.loads(response.content)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_clients_not_exists_404(api_client, create_client):
    response = api_client.delete(f'{URL}/clients/999/')
    assert response.status_code == status.HTTP_404_NOT_FOUND
