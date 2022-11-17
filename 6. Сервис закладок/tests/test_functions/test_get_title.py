from vcr import use_cassette

from bookmarker.utils.bookmark import get_page_title


class TestGetPageTitle:
    @use_cassette("tests/test_functions/html_examples/yandex.yaml")
    def test_get_page_with_title(self):
        assert get_page_title("https://yandex.net") == "Яндекс"

    def test_get_unreachable_page(self):
        assert get_page_title("https://unreachable_site.net") == "Unreachable page"

    @use_cassette("tests/test_functions/html_examples/untitled_site.yaml")
    def test_get_untitled_page(self):
        # Тут искусственный запрос в yandex.net.
        # Для него мы удалили всё из body и title страницы и положили ответ в untitled_site.yaml
        assert get_page_title("https://yandex.net") == "Untitled page"
