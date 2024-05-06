from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine

from app.core.config import settings
from app.dependencies import SessionLocal
from app.main import app
from app.tests.utils.utils import get_token_headers


@pytest.fixture(scope="session")
def engine():
    return create_engine(
        str(settings.SQLALCHEMY_DATABASE_URI), isolation_level="READ_COMMITTED"
    )


@pytest.fixture(scope="function")
def db_test(engine):
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def logged_user(client: TestClient) -> dict[str, str]:
    return get_token_headers(client)
