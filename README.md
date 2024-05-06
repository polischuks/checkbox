## Checkbox Project
## Overview
The Checkbox project leverages a modern technology stack to deliver a fast and secure API service. Built with FastAPI, it benefits from asynchronous request handling and automatic data validation using Pydantic models. This project is ideal for applications requiring robust database interactions and secure authentication mechanisms.

## Technology Stack and Features

- ⚡ [**FastAPI**](https://fastapi.tiangolo.com) for the Python backend API.
    - 🧰 [SQLModel](https://sqlmodel.tiangolo.com) for the Python SQL database interactions (ORM).
    - 🔍 [Pydantic](https://docs.pydantic.dev), used by FastAPI, for the data validation and settings management.
    - 💾 [PostgreSQL](https://www.postgresql.org) as the SQL database.
- 🐋 [Docker Compose](https://www.docker.com) for development and production.
- 🔒 Secure password hashing by default.
- 🔑 JWT token authentication.
- ✅ Tests with [Pytest](https://pytest.org).

## Quick Start
### Clone the repository:

```bash
git clone https://github.com/polischuks/checkbox.git
cd checkbox
```
### Install Dependencies:
    
```bash
poetry install
```

### Run tests

Ensure everything is set up correctly.
Tests are run by [`pytest`](https://docs.pytest.org/en/latest/) framework:

```bash
$ pytest
```

## Deployment with Docker
Deploying the Checkbox application with Docker is straightforward:

### Build the Docker image:

```bash
docker-compose build
```

### Run the Docker container:

```bash
docker-compose up -d
```

## Access the API

The API is now accessible at http://localhost:8000.

## API Documentation
The API documentation is available at http://localhost:8000/docs

## Contributing
Contributions are welcome! Please feel free to submit a pull request.


## Setup pre-commit hooks

```
pre-commit install
```
