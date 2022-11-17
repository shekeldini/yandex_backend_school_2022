import datetime

import pytest
from freezegun import freeze_time
from starlette import status

from shortener.utils import get_now_date, url_from_suffix


pytestmark = pytest.mark.asyncio


class TestMakeShorterHandler:
    @staticmethod
    def get_url() -> str:
        return "/api/v1/make_shorter"

    @pytest.mark.parametrize(
        "url, expected_status",
        (
            ("https://yandex.ru", status.HTTP_200_OK),
            ("some-bad-url", status.HTTP_422_UNPROCESSABLE_ENTITY),
        ),
    )
    async def test_base_scenario(self, client, url, expected_status):
        data = {"url": url}
        response = await client.post(url=self.get_url(), json=data)
        assert response.status_code == expected_status

    async def test_duplicate(self, client, data_sample):
        data = {"url": data_sample.long_url}
        response = await client.post(url=self.get_url(), json=data)
        assert response.status_code == status.HTTP_200_OK

    async def test_vip_scenario(self, client):
        data = {"url": "https://example.com/vip", "vip_key": "example_vip"}
        response = await client.post(url=self.get_url(), json=data)
        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert response_data["short_url"] == url_from_suffix(data["vip_key"])
        assert "secret_key" in response_data

        response = await client.post(url=self.get_url(), json=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    async def test_time_to_live_maximum(self, client):
        data = {
            "url": "https://example.com/ttl_max",
            "vip_key": "example_ttl_max",
            "time_to_live": 49,  # HOURS - default unit
        }
        response = await client.post(url=self.get_url(), json=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        data["time_to_live"] = 48
        response = await client.post(url=self.get_url(), json=data)
        assert response.status_code == status.HTTP_200_OK

    async def test_time_to_live_expiration(self, client):
        data = {
            "url": "https://example.com/ttl_exp",
            "vip_key": "example_ttl_exp",
            "time_to_live": 1,
            "time_to_live_unit": "SECONDS",
        }

        with freeze_time(datetime.datetime.now()) as frozen_datetime:
            response = await client.post(url=self.get_url(), json=data)
            assert response.status_code == status.HTTP_200_OK

            response_data = response.json()
            response = await client.get(url=response_data["short_url"])
            assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
            frozen_datetime.tick(delta=datetime.timedelta(seconds=2))
            response = await client.get(url=response_data["short_url"])
            assert response.status_code == status.HTTP_404_NOT_FOUND
