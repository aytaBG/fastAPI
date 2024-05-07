import datetime

from sqlalchemy import Column, Integer, String, TIMESTAMP

from src import Base


# таблица операций для бд
class OperationModel(Base):
    # название
    __tablename__ = 'operation'
    # столбцы
    # номер операции, дополняется автоматически
    id = Column(Integer, primary_key=True)
    quantity = Column(String)
    figi = Column(String)
    instrument_type = Column(String, nullable=False)
    date = Column(TIMESTAMP(timezone=True))
    type = Column(String)
