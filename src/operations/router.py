import time

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.operations.models import OperationModel
from src.operations.schemas import OperationCreate


operation = OperationModel.__table__


router = APIRouter(
    prefix='/operations',
    tags=['Operation']
)


@router.get('/long_operation')
@cache(expire=30)
def get_long_op():
    time.sleep(2)
    return 'Abba abbA'


@router.get('')
async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(operation).where(operation.c.type == operation_type)
        result = await session.execute(query)
        return {
            'status': 'success',
            'data': result.mappings().all(),
            'details': None
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': None,
            'details': None
        })


@router.post('')
async def add_specific_operations(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = insert(operation).values(**new_operation.model_dump())
        await session.execute(stmt)
        await session.commit()
        return {
            'status': 'success',
            'data': None,
            'details': None
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': None,
            'details': None
        })
