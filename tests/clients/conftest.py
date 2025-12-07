import pytest
from rest_framework.test import APIClient

from clients.models.cliente import Cliente


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def clientes(db):
    c1 = Cliente.objects.create(nombre="Juan", documento="123", zona="norte")
    c2 = Cliente.objects.create(nombre="Pedro", documento="987", zona="sur")
    return c1, c2
