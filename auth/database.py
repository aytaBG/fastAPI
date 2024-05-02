import datetime
from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase

from sqlalchemy import String, Boolean, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from config import DB_USER, DB_PASS, DB_NAME, DB_PORT, DB_HOST
from models.models import role


# адрес базы данных для FastAPI Users
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


class Base(DeclarativeBase):
    pass


# модель пользователя
class User(SQLAlchemyBaseUserTable[int], Base):
    # номер пользователя, дополняется автоматически
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    # имейл, обязателен
    email: Mapped[str] = mapped_column(
        String, nullable=False
    )
    # юзернейм, обязателен
    username: Mapped[str] = mapped_column(
        String, nullable=False
    )
    # время регистрации, атоматичести ставится текущее время в поясе UTC
    registered_at: Mapped[str] = mapped_column(
        TIMESTAMP, default=datetime.datetime.utcnow()
    )
    # роль, ссылка на таблицу role столбец id
    role_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(role.c.id)
    )
    # закодированный пароль, обязателен
    hashed_password: Mapped[str] = mapped_column(
        String, nullable=False
    )
    # атрибуты из класса SQLAlchemyBaseUserTable
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )


# точка входа SQLAlchemy в бд
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


# получение модели пользователя
async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
