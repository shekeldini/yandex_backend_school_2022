from app.services.strategies import RoundRobin
from tests.utils import get_available_services


class TestRoundRobin:
    async def test_create_token(self, token, service_statistic, mock_service_statistic):
        strategy = RoundRobin(
            available_services=get_available_services(),
            statistics=service_statistic
        )
        status_code, response_token = await strategy.create_token(token)

        valid_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9." \
                      "eyJpZCI6InRlc3QiLCJ0aW1lc3RhbXAiOjB9." \
                      "RX8VMur1EMCF1cp8rlDuNn8jMsVyiSU8Mv00UbTGYZU"

        assert valid_token == response_token
