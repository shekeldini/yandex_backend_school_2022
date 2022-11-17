from starlette import status


class TestPing:
    async def test_ping_application(self, client):
        response = await client.get("api/v1/health_check/ping_application")
        assert response.status_code == status.HTTP_200_OK

    async def test_ping_database(self, client):
        response = await client.get("api/v1/health_check/ping_database")
        assert response.status_code == status.HTTP_200_OK

    async def test_ping_database_with_error(self, client, set_wrong_port_for_postgres):  # pylint: disable=W0613
        response = await client.get("api/v1/health_check/ping_database")
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
