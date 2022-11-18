from datetime import timedelta

import pytest
from jose import jwt
from bookmarker.config import get_settings
from bookmarker.utils.user import create_access_token

pytestmark = pytest.mark.asyncio


class TestCreateAccessToken:
    async def test_create_access_token(self):
        access_token_expires = timedelta(minutes=get_settings().ACCESS_TOKEN_EXPIRE_MINUTES)
        sub = "test_name"
        token = create_access_token(
            data={"sub": sub},
            expires_delta=access_token_expires
        )
        payload = jwt.decode(token, get_settings().SECRET_KEY, algorithms=[get_settings().ALGORITHM])
        username: str = payload.get("sub")
        assert sub == username
