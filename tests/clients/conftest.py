from datetime import date
from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from clients.models.cliente import Cliente
from clients.models.deuda import Deuda
from clients.models.portafolio import Portafolio

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(username="test", password="1234")


@pytest.fixture
def auth_client(api_client, user):
    refresh = RefreshToken.for_user(user)
    access = str(refresh.access_token)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
    return api_client


@pytest.fixture
def clientes(db):
    c1 = Cliente.objects.create(nombre="Juan", documento="123", zona="norte")
    c2 = Cliente.objects.create(nombre="Pedro", documento="987", zona="sur")
    return c1, c2


@pytest.fixture
def cliente(db):
    return Cliente.objects.create(
        nombre="Carlos",
        documento="321",
        zona="oeste",
    )


@pytest.fixture
def deuda(db, cliente):
    return Deuda.objects.create(
        cliente=cliente,
        monto=Decimal("5000000.00"),
        vencimiento=date(2025, 12, 12),
        tipo="Personal",
    )


@pytest.fixture
def portafolio(db, cliente):
    return Portafolio.objects.create(
        cliente=cliente,
        tipo="Ahorro",
        monto=Decimal("10000000.00"),
    )
