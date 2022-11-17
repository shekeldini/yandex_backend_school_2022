from logging import getLogger
from socket import gaierror
from urllib.error import URLError
from urllib.request import urlopen

from bs4 import BeautifulSoup


logger = getLogger(__name__)


def get_page_title(page_url: str) -> str:
    try:
        # Без features="html.parser" вы бы получали warning-и в консоли
        soup = BeautifulSoup(urlopen(page_url), features="html.parser")
    # ERROR: убираем проблемы, связанные с недоступностью сайта и наличием на сайте заголовка
    # Если это не убрать, сервис валится на том, что заголовок в базе должен быть не nullable
    except (
        URLError,
        gaierror,
    ) as exc:
        logger.warning("Error in get_page_title: %s", exc)
        return "Unreachable page"
    return getattr(getattr(soup, "title"), "string", "Untitled page")
