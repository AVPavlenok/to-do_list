import os

import pytest
import pytest_asyncio

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from settings import settings, logger
from src.models import Base, User
from src.routers import create_app
from tests.demo_data import load_demo_db

DB_URL = "sqlite+aiosqlite:///test.db"
# DB_URL = f"postgresql+asyncpg://" \
#          f"{settings.postgres_user}:{settings.postgres_password}@localhost:5432/{settings.postgres_db}"


@pytest_asyncio.fixture(scope="session", autouse=True)
async def client():
    engine = create_async_engine(DB_URL)
    async_session = async_sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    session = async_session()
    app = create_app(engine_db=engine, session_db=session)
    logger.debug(f'app: {app.__dict__}')
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # await load_demo_db(session=session)

    yield TestClient(app)

    await session.close()
    await engine.dispose()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    os.remove("./test.db")


def test_hello_world(client):
    response = client.get("http://localhost:8080")
    assert response.status_code == 200


def test_register_user(client):
    data = {
        "name": "name4",
        "login": 'login4',
        'password': 'password4'
    }

    response = client.post("http://localhost:8080/register", json=data)

    assert response.status_code == 201


def test_register_dublicate_user(client):
    data = {
        "name": "name4",
        "login": 'login4',
        'password': 'password4'
    }

    response = client.post("http://localhost:8080/register", json=data)
    assert response.status_code == 409


def test_login(client):
    data = {
        "login": 'login4',
        'password': 'password4'
    }
    response = client.post("http://localhost:8080/login", json=data)

    assert response.status_code == 200


def test_add_task(client):
    data = [
        {
            'task': 'New test task #1',
        },
        {
            'task': 'New test task #2',
        }
    ]
    for item in data:
        response = client.post("http://localhost:8080/tasks", json=item)

        assert response.status_code == 201


def test_complete_task(client):
    response = client.patch("http://localhost:8080/tasks/1")

    assert response.status_code == 200


def test_get_all_tasks(client):
    response = client.get("http://localhost:8080/tasks")

    assert len(response.json()) == 2


def test_get_actual_tasks(client):
    response = client.get("http://localhost:8080/tasks/actual")

    assert len(response.json()) == 1


def test_task_by_id(client):
    response = client.get("http://localhost:8080/tasks/1")

    assert response.status_code == 200


def test_delete_task(client):
    response = client.delete('http://localhost:8080/tasks/1')

    assert response.status_code == 200


def test_logout(client):
    response = client.post('http://localhost:8080/logout')

    assert response.status_code == 200
