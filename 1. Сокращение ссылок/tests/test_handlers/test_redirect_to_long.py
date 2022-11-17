import pytest
from starlette import status

from shortener.db.models import UrlStorage


pytestmark = pytest.mark.asyncio


class TestRedirectToLongHandler:
    @staticmethod
    def get_url(short_code: str) -> str:
        return f"/api/v1/{short_code}"

    async def test_not_found(self, client):
        short_url = "12345"
        response = await client.get(url=self.get_url(short_url))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_main_scenario(self, client, data_sample, database):
        response = await client.get(url=self.get_url(data_sample.short_url))
        assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT

        object_in_base = database.query(UrlStorage).where(UrlStorage.short_url == data_sample.short_url).first()
        database.refresh(object_in_base)
        assert object_in_base.number_of_clicks == 1
