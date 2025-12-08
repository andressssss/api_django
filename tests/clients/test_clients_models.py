from datetime import date

import pytest

from clients.models.cliente import Cliente
from clients.models.deuda import Deuda
from clients.models.portafolio import Portafolio


@pytest.mark.django_db
def test_str_cliente():
    cliente = Cliente.objects.create(
        nombre="Juan Perez", documento="123456789", zona="norte"
    )
    assert str(cliente) == "Juan Perez"


@pytest.mark.django_db
def test_crear_deuda(cliente):
    deuda = Deuda.objects.create(
        cliente=cliente,
        monto=1000.50,
        vencimiento=date(2025, 1, 1),
        tipo="prestamo",
    )
    assert deuda.id is not None
    assert deuda.cliente == cliente
    assert deuda.monto == 1000.50
    assert deuda.estado == "pendiente"


@pytest.mark.django_db
def test_crear_portafolio(cliente):
    p = Portafolio.objects.create(
        cliente=cliente,
        tipo="inversion",
        monto=5000.00,
    )
    assert p.id is not None
    assert p.cliente == cliente
    assert p.tipo == "inversion"
    assert p.datos == {}
