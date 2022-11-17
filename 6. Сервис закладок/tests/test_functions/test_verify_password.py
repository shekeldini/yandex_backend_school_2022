from typing import Any
from uuid import uuid4

import pytest
from passlib.context import CryptContext

from bookmarker.config import get_settings
from bookmarker.utils.user import verify_password


class TestVerifyPassword:
    @staticmethod
    def prepare_correct_hashed_password() -> tuple[str, Any]:
        settings = get_settings()
        pwd_context = settings.PWD_CONTEXT

        password = str(uuid4())
        hashed_password = pwd_context.hash(password)
        return password, hashed_password

    @staticmethod
    def prepare_incorrect_hashed_password() -> tuple[str, Any]:
        pwd_context = CryptContext(schemes=["sha256_crypt", "des_crypt"])

        password = str(uuid4())
        hashed_password = pwd_context.hash(password)
        return password, hashed_password

    @pytest.mark.parametrize(
        "passwords, verdict",
        (
            (prepare_correct_hashed_password(), True),
            (prepare_incorrect_hashed_password(), False),
        ),
    )
    def test_verify_password(self, passwords, verdict):
        assert verify_password(passwords[0], passwords[1]) is verdict
