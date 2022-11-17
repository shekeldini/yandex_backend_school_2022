from starlette import status
from tests.utils import generate_timestamp, generate_id


class TestToken:
    async def test_token(self, client):
        response = await client.get(f"token?id={generate_id()}&timestamp={generate_timestamp()}")
        assert response.status_code == status.HTTP_200_OK

    async def test_token_without_id(self, client):
        response = await client.get(f"token?timestamp={generate_timestamp()}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.text == "Request is missing required query parameter 'id'"

    async def test_token_without_timestamp(self, client):
        response = await client.get(f"token?id={generate_id()}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.text == "Request is missing required query parameter 'timestamp'"

    async def test_service_unavailable(self, client, mock_create_token, mock_get_service_list):
        response = await client.get(f"token?id={generate_id()}&timestamp={generate_timestamp()}")
        assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
        assert response.text == "Service Unavailable"

