from sqlalchemy import delete, exc, select
from sqlalchemy.ext.asyncio import AsyncSession

from bookmarker.db.models import User
from bookmarker.schemas import RegistrationForm


async def get_user(session: AsyncSession, username: str) -> User | None:
    query = select(User).where(User.username == username)
    return await session.scalar(query)


async def register_user(session: AsyncSession, potential_user: RegistrationForm) -> tuple[bool, str]:
    user = User(**potential_user.dict(exclude_unset=True))
    session.add(user)
    try:
        await session.commit()
    except exc.IntegrityError:
        return False, "Username already exists."
    return True, "Successful registration!"


async def delete_user(session: AsyncSession, user: User) -> None:
    query = delete(User).where(User.username == user.username)
    await session.execute(query)
    await session.commit()
