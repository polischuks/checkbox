from fastapi.testclient import TestClient
from app.core.config import settings


def test_get_access_token(client: TestClient) -> None:
    """
    Test that we can get an access token
    :param client:
    :return:
    """

    login_data = {
        "username": settings.FIRST_LOGIN,
        "password": settings.FIRST_PASSWORD,
    }
    url = f"http://{settings.DOMAIN}:8000/token"
    r = client.post(url, data=login_data)
    tokens = r.json()
    assert r.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]


def test_no_get_access_token_incorrect_password(client: TestClient) -> None:
    """
    Test that we cannot get an access token with an incorrect password
    :param client:
    :return:
    """

    login_data = {
        "username": settings.FIRST_LOGIN,
        "password": "incorrect",
    }
    r = client.post(f"http://{settings.DOMAIN}:8000/token", data=login_data)
    assert r.status_code == 401

