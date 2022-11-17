from bookmarker.utils.common import get_hostname


class TestGetHostname:
    def test_host_for_app(self):
        # Подобные тесты излишни, потому что по факту мы тестируем библиотечную функцию
        # (но coverage +0,01% это конечно даст)
        host = "https://127.0.0.1/?"
        assert get_hostname(host) == "127.0.0.1"
