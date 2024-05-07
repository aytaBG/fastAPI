from time import sleep

import pytest

from httpx import AsyncClient


@pytest.mark.operation
class TestGetOperation():
    @pytest.fixture(scope='class', autouse=True)
    async def add_specific_operations(self, ac: AsyncClient):
        await ac.post("/operations", json={
            "id": 1,
            "quantity": "25.5",
            "figi": "figi_CODE",
            "instrument_type": "bond",
            "date": "2023-02-01T00:00:00",
            "type": "Выплата купонов",
        })

        yield

    @pytest.mark.skip
    async def test_get_specific_operations(self, ac: AsyncClient):
        response = await ac.get("/operations", params={
            'operation_type': "Выплата купонов",
        })
        sleep(10)
        assert response.status_code == 200
        assert response.json()["status"] == "success"
        assert len(response.json()["data"]) == 1