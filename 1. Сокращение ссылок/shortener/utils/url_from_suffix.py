from shortener.utils.get_settings import get_settings


def url_from_suffix(suffix: str) -> str:
    settings = get_settings()
    short_url = f"{settings.APP_HOST}:{settings.APP_PORT}{settings.PATH_PREFIX}/{suffix}"
    return short_url
