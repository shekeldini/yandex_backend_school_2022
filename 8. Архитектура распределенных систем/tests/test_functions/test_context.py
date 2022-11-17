from tests.utils.context import get_context


class TestContext:
    async def test_create_token(self, token, mock_get_service_list, mock_create_request):
        context = get_context()
        valid_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9." \
                      "eyJpZCI6InRlc3QiLCJ0aW1lc3RhbXAiOjB9." \
                      "RX8VMur1EMCF1cp8rlDuNn8jMsVyiSU8Mv00UbTGYZU"
        status_code, response_token = await context.create_token(
            token
        )
        assert valid_token == response_token
