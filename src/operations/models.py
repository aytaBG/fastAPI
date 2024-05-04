import datetime

from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, MetaData


# переменная для создания миграций alembic
metadata = MetaData()

# таблица операций для бд
operation = Table(
    # название
    'operation',
    # сохранение добавленной информации для миграции
    metadata,
    # столбцы
    # номер операции, дополняется автоматически
    Column('id', Integer, primary_key=True),
    Column('quantity', String),
    Column('figi', String),
    Column('instrument_type', String, nullable=False),
    Column('date', TIMESTAMP(timezone=True)),
    Column('type', String),
)