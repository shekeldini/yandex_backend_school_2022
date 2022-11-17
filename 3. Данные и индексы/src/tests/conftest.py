import sys
import pytest

from rest_framework.test import APIClient


def make_client():
    client = APIClient()
    return client


@pytest.fixture
def user():
    return make_client()


@pytest.mark.django_db
def read_indexes(cursor):
    solutions = (
        # проверяем 1е два решения
        "../solution/task_v1.sql",
        "../solution/task_v2.sql",
        # вдруг есть один файл с решениями
        "../solution/solution.sql",
    )

    for file in solutions:
        try:
            with open(file) as sql:
                raw_sql = sql.read()
                if raw_sql:
                    cursor.execute(raw_sql)
        except Exception as e:
            # локально миграции не применятся
            ...


@pytest.fixture(scope="session")
def django_db_setup(django_db_blocker):
    from django.db import connection

    with django_db_blocker.unblock():
        with connection.cursor() as cursor:
            read_indexes(cursor)
            cursor.execute("select pg_stat_reset();")
