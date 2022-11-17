import pytest

from bookmarker.config import DefaultSettings, get_settings


class TestGetSettings:
    @pytest.mark.parametrize(
        "env_value, expected_class",
        [(None, DefaultSettings), ("local", DefaultSettings), ("non_existent", DefaultSettings)],
    )
    def test_get_settings(self, monkeypatch, env_value, expected_class):
        if env_value is not None:
            monkeypatch.setenv("ENV", env_value)
        else:
            monkeypatch.delenv("ENV", raising=False)
        settings = get_settings()
        assert isinstance(settings, expected_class)
