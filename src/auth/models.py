import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from sqlalchemy import MetaData, Integer, String, TIMESTAMP, ForeignKey, Table, Column, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base

# переменная для создания миграций alembic
metadata = MetaData()

# таблица ролей для б/д
role = Table(
    # название
    'role',
    # сохранение добавленной информации для миграции
    metadata,
    # столбцы
    # номер роли, дополняется автоматически
    Column('id', Integer, primary_key=True),
    # название роли, обязательно
    Column('name', String, nullable=False),
    # разрешения роли
    Column('permissions', JSON)
)

# таблица пользователей
user = Table(
    # название
    'user',
    # сохранение добавленной информации для миграции
    metadata,
    # столбцы
    # номер пользователя, дополняется автоматически
    Column('id', Integer, primary_key=True),
    # имейл, обязателен
    Column('email', String, nullable=False),
    # юзернейм, обязателен
    Column('username', String, nullable=False),
    # закодированный пароль, обязателен
    Column('hashed_password', String, nullable=False),
    # время регистрации, атоматичести ставится текущее время в поясе UTC
    Column('registered_at', TIMESTAMP, default=datetime.datetime.utcnow()),
    # роль, ссылка на таблицу role столбец id
    Column('role_id', Integer, ForeignKey('role.id')),
    # столбцы из класса SQLAlchemyBaseUserTable
    Column('is_active', Boolean, default=True, nullable=False),
    Column('is_superuser', Boolean, default=False, nullable=False),
    Column('is_verified', Boolean, default=False, nullable=False),
)


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
