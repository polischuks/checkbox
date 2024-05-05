

## Technology Stack and Features

- ⚡ [**FastAPI**](https://fastapi.tiangolo.com) for the Python backend API.
    - 🧰 [SQLModel](https://sqlmodel.tiangolo.com) for the Python SQL database interactions (ORM).
    - 🔍 [Pydantic](https://docs.pydantic.dev), used by FastAPI, for the data validation and settings management.
    - 💾 [PostgreSQL](https://www.postgresql.org) as the SQL database.
- 🐋 [Docker Compose](https://www.docker.com) for development and production.
- 🔒 Secure password hashing by default.
- 🔑 JWT token authentication.
- ✅ Tests with [Pytest](https://pytest.org).

## Run tests

Tests are run by [`pytest`](https://docs.pytest.org/en/latest/) framework:

```bash
$ pytest
# or
$ make test
```

## Setup pre-commit hooks

```
pre-commit install
```
