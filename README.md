# FastAPI Books

FastAPI back-end for a simple CRUD books API.

## Tech Stack

- Python (≥ 3.10)
- FastAPI
- Pydantic
- SQLModel
- Alembic
- Docker

## Environment Variables

```text
POSTGRES_SERVER=
POSTGRES_PORT=
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=

DOCKER_IMAGE_BACKEND=
```

## Setup

1. Docker build (no registry)

```bash
docker build -t fastapi-books-backend:latest .
```

1. Docker compose

```bash
docker-compose up
```
