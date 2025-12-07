import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_list_clientes(api_client, clientes):
    c1, c2 = clientes
    list_url = reverse("cliente-list")
    response = api_client.get(list_url)
    assert response.status_code == 200
    assert len(response.data) == 2

@pytest.mark.django_db
def test_filter_by_zona(api_client, clientes):
    c1, c2 = clientes
    list_url = reverse("cliente-list")
    response = api_client.get(list_url, {"zona": "norte"})
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['nombre'] == "Juan"
