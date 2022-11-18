from urllib.error import URLError
from urllib.request import urlopen

from bs4 import BeautifulSoup


def get_page_title(page_url: str) -> str | None:
    try:
        soup = BeautifulSoup(urlopen(page_url), "html.parser")
    except URLError:
        return None
    return soup.title.string
