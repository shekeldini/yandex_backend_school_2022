import os
from pathlib import Path
from types import SimpleNamespace
from typing import Union
from fastapi import status
from alembic.config import Config
from configargparse import Namespace

PROJECT_PATH = Path(__file__).parent.parent.resolve()


def make_alembic_config(cmd_opts: Union[Namespace, SimpleNamespace], base_path: Path = PROJECT_PATH) -> Config:
    """
    Создает объект конфигурации alembic на основе аргументов командной строки,
    подменяет относительные пути на абсолютные.
    """
    path_to_folder = cmd_opts.config
    # Подменяем путь до файла alembic.ini на абсолютный
    if not os.path.isabs(cmd_opts.config):
        cmd_opts.config = os.path.join(base_path, cmd_opts.config + "alembic.ini")

    config = Config(file_=cmd_opts.config, ini_section=cmd_opts.name, cmd_opts=cmd_opts)

    # Подменяем путь до папки с alembic на абсолютный
    alembic_location = config.get_main_option("script_location")
    if not os.path.isabs(alembic_location):
        config.set_main_option("script_location", os.path.join(base_path, path_to_folder + alembic_location))
    if cmd_opts.pg_url:
        config.set_main_option("sqlalchemy.url", cmd_opts.pg_url)

    return config


async def auth_user(client, user_data_sample):
    data = {
        "username": user_data_sample.username,
        "password": "test",
    }
    response = await client.post(
        url='api/v1/user/authentication',
        data=data,
        headers={
            "content-type": "application/x-www-form-urlencoded",
            "accept": "application / json"
        }
    )
    return response.json()


async def create_item(client, user_data_sample, tag):
    response_data = await auth_user(client, user_data_sample)
    data = {
        "link": "https://vk.com/",
        "tag": tag
    }
    response = await client.post(
        url="/api/v1/bookmark",
        json=data,
        headers={"Authorization": f"Bearer {response_data['access_token']}", "accept": "application / json"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    return response.json(), response_data['access_token']


async def invalid_access_token_get(client, url):
    response = await client.get(
        url=url,
        headers={"Authorization": "Bearer ", "accept": "application / json"}
    )
    return response


async def invalid_access_token_delete(client, url):
    response = await client.delete(
        url=url,
        headers={"Authorization": "Bearer ", "accept": "application / json"}
    )
    return response
