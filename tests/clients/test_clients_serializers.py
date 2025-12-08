import pytest

from clients.serializers.cliente import ClienteSerializer
from clients.serializers.deuda import DeudaSerializer
from clients.serializers.portafolio import PortafolioSerializer


@pytest.mark.django_db
def test_cliente_serializer(cliente):
    data = ClienteSerializer(cliente).data

    assert data["nombre"] == cliente.nombre
    assert data["documento"] == cliente.documento
    assert data["zona"] == cliente.zona


@pytest.mark.django_db
def test_deuda_serializer(deuda):
    serializer = DeudaSerializer(deuda)
    data = serializer.data

    assert data["monto"] == format(deuda.monto, ".2f")
    assert data["tipo"] == deuda.tipo
    assert data["estado"] == deuda.estado


@pytest.mark.django_db
def test_portafolio_serializer(portafolio):
    serializer = PortafolioSerializer(portafolio)
    data = serializer.data

    assert data["tipo"] == portafolio.tipo
    assert data["monto"] == format(portafolio.monto, ".2f")
    assert data["datos"] == portafolio.datos
