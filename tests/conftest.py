import asyncio

from typing import AsyncGenerator

import pytest

from fastapi.testclient import TestClient

from httpx import AsyncClient, ASGITransport

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME_TEST
from src.database import get_async_session
from src.main import app
from src import Base

# адрес базы данных
DATABASE_URL_TEST = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME_TEST}"


metadata = Base.metadata


# точка входа SQLAlchemy в бд
engine_test = create_async_engine(DATABASE_URL_TEST)
async_session_maker = async_sessionmaker(engine_test, expire_on_commit=False)
metadata.bind = engine_test


async def override_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_async_session] = override_async_session


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)


client = TestClient(app)


@pytest.fixture(scope='session')
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test', follow_redirects=True) as ac:
        yield ac
