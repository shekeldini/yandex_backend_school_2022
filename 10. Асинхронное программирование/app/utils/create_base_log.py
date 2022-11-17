import json

from fastapi import Request
from app.config import get_settings


async def create_base_log(request: Request, data=False):
    log = {
        "client_ip": request.client.host,
        "method": request.method,
        "url": request.url.path + request.url.query,
        "service": get_settings().SERVICE_NAME
    }
    if data:
        log["request_json"] = await request.json()
    return log
