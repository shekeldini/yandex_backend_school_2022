import pytest
from bookmarker.utils.user import verify_password

pytestmark = pytest.mark.asyncio


class TestVerifyPassword:
    async def test_valid_password(self, user_data_sample):
        valid = verify_password("test", user_data_sample.password)
        assert valid is True

    async def test_invalid_password(self, user_data_sample):
        valid = verify_password("invalid", user_data_sample.password)
        assert valid is False
