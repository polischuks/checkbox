from fastapi.testclient import TestClient

from app.core.config import settings


def get_token_headers(client: TestClient) -> dict[str, str]:
    login_data = {
        "username": settings.FIRST_LOGIN,
        "password": settings.FIRST_PASSWORD,
    }
    url = f"http://{settings.DOMAIN}:8000/token"
    r = client.post(url, data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers
