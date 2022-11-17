from typing import Optional, Tuple, Any
from sqlalchemy.orm import Session
from app.utils.users import DoctorAccount, UserAccount
from app.repositories.accounts import BaseRepository


async def get_user(user_id: int, db: Session) -> Tuple[Optional[BaseRepository], Any]:
    """
    Обычно клиентский код приспособлен для работы с единственным обработчиком. В
    большинстве случаев клиенту даже неизвестно, что этот обработчик является
    частью цепочки.
    """
    doctor = DoctorAccount()
    user = UserAccount()

    # создание цепочки
    doctor.set_next(user)

    repositories, user = await doctor.handle(user_id, db)
    return repositories, user
