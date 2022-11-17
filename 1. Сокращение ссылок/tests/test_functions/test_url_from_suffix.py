from uuid import uuid4

import pytest
from mock import Mock

from shortener.config import DefaultSettings
from shortener.utils import url_from_suffix


pytestmark = pytest.mark.asyncio


class TestFunctionUrlFromSuffix:
    async def test_with_default_settings(self, client):
        mock_settings = Mock("shortener.utils.get_settings")
        mock_settings.return_value = DefaultSettings()

        suffix = uuid4().hex
        url = url_from_suffix(suffix)
        assert url == f"http://127.0.0.1:8080/api/v1/{suffix}"
