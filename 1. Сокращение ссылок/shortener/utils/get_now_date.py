import datetime


def get_now_date() -> datetime:
    return datetime.datetime.now(tz=datetime.timezone.utc)
