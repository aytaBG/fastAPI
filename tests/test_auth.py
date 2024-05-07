from time import sleep

import pytest

from sqlalchemy import insert, select

from src.auth.models import RoleModel
from tests.conftest import client, async_session_maker


role = RoleModel.__table__


@pytest.mark.auth
class TestRegister:
    @pytest.fixture(scope='class', autouse=True)
    async def add_role(self):
        async with async_session_maker() as session:
            stmt = insert(role).values(id=1, name='admin', permissions=None)
            await session.execute(stmt)
            await session.commit()

            query = select(role)
            print(query)
            result = await session.execute(query)
            print(result.mappings().all())
            yield

    def test_register(self):
        response = client.post('/auth/register', json={
            "email": "string",
            "password": "string",
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
            "username": "string",
            "role_id": 0
        })

        assert response.status_code == 201, 'Ошибка регистрации'


