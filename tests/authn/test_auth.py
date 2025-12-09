import time
from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


@pytest.fixture(autouse=True)
def disable_throttling(settings):
    settings.REST_FRAMEWORK["DEFAULT_THROTTLE_CLASSES"] = []


# ---------------------------
# FIXTURES
# ---------------------------


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="1234")


@pytest.fixture
def auth_urls():
    return {
        "login": reverse("token_obtain_pair"),
        "refresh": reverse("token_refresh"),
        "logout": reverse("token_blacklist"),
        "protected": reverse("secure-endpoint"),
    }


# ---------------------------
# TESTS JWT
# ---------------------------


# LOGIN OK
def test_login_ok(api_client, user, auth_urls):
    response = api_client.post(
        auth_urls["login"], {"username": "testuser", "password": "1234"}
    )

    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data


# LOGIN INCORRECTO
def test_login_invalid(api_client, user, auth_urls):
    response = api_client.post(
        auth_urls["login"], {"username": "testuser", "password": "wrong"}
    )

    assert response.status_code == 401


# REFRESH OK
def test_refresh_ok(api_client, user, auth_urls):
    tokens = RefreshToken.for_user(user)

    response = api_client.post(auth_urls["refresh"], {"refresh": str(tokens)})

    assert response.status_code == 200
    assert "access" in response.data


# REFRESH INVÁLIDO
def test_refresh_invalid(api_client, auth_urls):
    response = api_client.post(
        auth_urls["refresh"], {"refresh": "invalid_refresh_token"}
    )

    assert response.status_code == 401


# LOGOUT / BLACKLIST
def test_logout_revokes_refresh(api_client, user, auth_urls):
    tokens = RefreshToken.for_user(user)

    # Logout → se invalida
    response = api_client.post(auth_urls["logout"], {"refresh": str(tokens)})

    assert response.status_code == 200

    # Intentar refrescar → falla
    response2 = api_client.post(auth_urls["refresh"], {"refresh": str(tokens)})

    assert response2.status_code == 401


# ENDPOINT PROTEGIDO SIN TOKEN
def test_protected_without_token(api_client, auth_urls):
    response = api_client.get(auth_urls["protected"])
    assert response.status_code == 401


# ENDPOINT PROTEGIDO CON TOKEN VÁLIDO
def test_protected_with_token(api_client, user, auth_urls):
    tokens = RefreshToken.for_user(user)
    access = str(tokens.access_token)

    response = api_client.get(
        auth_urls["protected"], HTTP_AUTHORIZATION=f"Bearer {access}"
    )

    assert response.status_code == 200


# ACCESS EXPIRADO + REFRESH OK
def test_access_expired_but_refresh_ok(api_client, user, auth_urls):
    tokens = RefreshToken.for_user(user)
    access = tokens.access_token

    # Expira en 1 segundo
    access.set_exp(lifetime=timedelta(seconds=1))
    expired_access = str(access)

    # Esperar para que expire
    time.sleep(2)

    # Access expirado → 401
    response = api_client.get(
        auth_urls["protected"], HTTP_AUTHORIZATION=f"Bearer {expired_access}"
    )
    assert response.status_code == 401

    # Refrescar → ok
    response2 = api_client.post(auth_urls["refresh"], {"refresh": str(tokens)})

    assert response2.status_code == 200
    assert "access" in response2.data


# REFRESH EN BLACKLIST
def test_refresh_blacklisted(api_client, user, auth_urls):
    tokens = RefreshToken.for_user(user)

    # Logout → blacklist
    api_client.post(auth_urls["logout"], {"refresh": str(tokens)})

    # Intentar usarlo → falla
    response = api_client.post(auth_urls["refresh"], {"refresh": str(tokens)})

    assert response.status_code == 401
