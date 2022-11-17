from asyncio.exceptions import TimeoutError as AsyncioTimeoutError

from aiohttp import ClientConnectorError, ClientSession, ClientTimeout


async def check_website_exist(url: str) -> tuple[bool, str]:
    timeout = ClientTimeout(total=2.0)
    try:
        async with ClientSession(timeout=timeout, connector_owner=False) as session:
            async with session.get(url) as response:
                if response.status < 400:
                    return True, "Status code < 400"
                return False, "Status code >= 400"
    except AsyncioTimeoutError:
        return False, "TimeoutError"
    except ClientConnectorError:
        return False, "ClientConnectorError"
