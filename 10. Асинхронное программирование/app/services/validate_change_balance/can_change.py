from app.services.validate_change_balance.handlers import Approve, NotNegative


async def can_change(*args, **kwargs) -> bool:
    """
    Обычно клиентский код приспособлен для работы с единственным обработчиком. В
    большинстве случаев клиенту даже неизвестно, что этот обработчик является
    частью цепочки.
    """
    approve = Approve()
    not_negative = NotNegative()

    approve.set_next(not_negative)
    status = await approve.handle(*args, **kwargs)
    return status
