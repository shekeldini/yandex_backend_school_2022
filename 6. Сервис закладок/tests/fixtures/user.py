from pytest import fixture

from tests.utils import UserFactory

from bookmarker.config import get_settings
from bookmarker.db.models import User
from bookmarker.utils.user import create_access_token


@fixture
async def user_with_auth_token(session) -> dict:
    user = UserFactory()
    settings = get_settings()
    hashed_password = settings.PWD_CONTEXT.hash(user.password)

    user_in_base = User(username=user.username, password=hashed_password)
    session.add(user_in_base)
    await session.commit()
    await session.refresh(user_in_base)

    access_token = create_access_token({"sub": user.username})

    return {
        "model": user_in_base,
        "header": {"Authorization": f"bearer {access_token}"},
        "password": user.password,
    }
