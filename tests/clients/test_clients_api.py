import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_list_clientes(auth_client, clientes):
    list_url = reverse("cliente-list")
    response = auth_client.get(list_url)

    assert response.status_code == 200
    assert len(response.data) == 2


@pytest.mark.django_db
def test_filter_by_zona(auth_client, clientes):
    list_url = reverse("cliente-list")
    response = auth_client.get(list_url, {"zona": "norte"})

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["nombre"] == "Juan"


@pytest.mark.django_db
def test_filter_by_documento(auth_client, clientes):
    list_url = reverse("cliente-list")

    response = auth_client.get(list_url, {"documento": "123"})

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["documento"] == "123"


@pytest.mark.django_db
def test_filter_by_ids(auth_client, clientes):
    c1, c2 = clientes
    list_url = reverse("cliente-list")

    response = auth_client.get(list_url, {"ids": f"{c1.id}"})

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["id"] == c1.id


@pytest.mark.django_db
def test_filter_by_ids_empty(auth_client, clientes):
    list_url = reverse("cliente-list")

    response = auth_client.get(list_url, {"ids": ""})

    assert response.status_code == 200
    assert len(response.data) == 2


@pytest.mark.django_db
def test_cliente_deudas_post_invalid(auth_client, clientes):
    cliente = clientes[0]
    url = reverse("cliente-deudas", args=[cliente.id])

    response = auth_client.post(
        url, {"monto": "bad-value", "vencimiento": "2025-12-12", "tipo": "Personal"}
    )

    assert response.status_code == 400
    assert "monto" in response.data


@pytest.mark.django_db
def test_cliente_deudas_get(auth_client, cliente, deuda):
    url = reverse("cliente-deudas", args=[cliente.id])

    response = auth_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["monto"] == format(deuda.monto, ".2f")


@pytest.mark.django_db
def test_cliente_deudas_post_valid(auth_client, cliente):
    url = reverse("cliente-deudas", args=[cliente.id])

    payload = {
        "monto": "1500.00",
        "vencimiento": "2025-10-10",
        "tipo": "prueba",
    }

    response = auth_client.post(url, payload)

    assert response.status_code == 201, response.data
    assert response.data["monto"] == "1500.00"
    assert response.data["tipo"] == "prueba"


@pytest.mark.django_db
def test_cliente_portafolios(auth_client, cliente, portafolio):
    url = reverse("cliente-portafolios", args=[cliente.id])

    response = auth_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["tipo"] == portafolio.tipo
