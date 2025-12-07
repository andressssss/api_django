import pytest
from clients.models.cliente import Cliente


@pytest.mark.django_db
def test_str_cliente():
    cliente = Cliente.objects.create(
        nombre="Juan Perez", documento="123456789", zona="norte"
    )
    assert str(cliente) == "Juan Perez"


@pytest.mark.django_db
def test_zona_value():
    cliente = Cliente.objects.create(
        nombre="Juan Perez", documento="123456789", zona="norte"
    )
    assert cliente.zona == "norte"
