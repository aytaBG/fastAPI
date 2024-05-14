import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from sqlalchemy import Integer, String, TIMESTAMP, ForeignKey, Column, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from src import Base


# таблица ролей для б/д
class RoleModel(Base):
    # название
    __tablename__ = 'role'
    # столбцы
    # номер роли, дополняется автоматически
    id = Column(Integer, primary_key=True)
    # название роли, обязательно
    name = Column(String, nullable=False)
    # разрешения роли
    permissions = Column(JSON)


# модель пользователя
class User(SQLAlchemyBaseUserTable[int], Base):
    # название
    __tablename__ = 'user'
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
        TIMESTAMP(timezone=True), default=datetime.datetime.now(datetime.UTC)
    )
    # роль, ссылка на таблицу role столбец id
    role_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("role.id", ondelete="CASCADE")
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
