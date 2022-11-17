from datetime import datetime, timedelta

from freezegun import freeze_time
from jose import jwt

from tests.utils import UserFactory

from bookmarker.config import get_settings
from bookmarker.utils.user import create_access_token


class TestCreateAccessToken:
    @staticmethod
    def prepare_data() -> dict[str, str]:
        return {"sub": UserFactory().username}

    def test_without_expires_delta(self):
        settings = get_settings()
        data = self.prepare_data()
        encoded_jwt = create_access_token(data=data)
        assert isinstance(encoded_jwt, str)
        decoded_jwt = jwt.decode(encoded_jwt, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        assert decoded_jwt["sub"] == data["sub"]
        assert decoded_jwt.get("exp", None) is not None

    # freeze_time нужен, чтобы при вычислении datetime.utcnow внутри функции и внутри теста получать одинаковые значения
    @freeze_time("2012-01-14")
    def test_with_expires_delta(self):
        settings = get_settings()
        data = self.prepare_data()
        exp = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES + 10)
        encoded_jwt = create_access_token(data=data, expires_delta=exp)
        assert isinstance(encoded_jwt, str)
        decoded_jwt = jwt.decode(encoded_jwt, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        assert decoded_jwt["sub"] == data["sub"]
        assert decoded_jwt.get("exp", None) == (exp + datetime.utcnow()).timestamp()
