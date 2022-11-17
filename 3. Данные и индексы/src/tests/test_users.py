import time
from functools import wraps

import pytest


def timeit(duration):
    def wrapper(method):
        @wraps(method)
        def timed(*args, **kwargs):
            # прогрев
            result = method(*args, **kwargs)
            ts = time.time()
            result = method(*args, **kwargs)
            te = time.time()
            execute_time = int((te - ts) * 1000)
            assert execute_time < duration

            return result

        return timed

    return wrapper


@pytest.mark.django_db
def test():
    """Показывает время выполнения без SQL запросов"""
    assert True is True


@pytest.mark.django_db
@pytest.mark.parametrize(
    "search",
    ("Josh", "Иван", "Dunin", "NotFoundValue"),
)
@timeit(duration=20)
def test_v1(user, search):
    response = user.get(f"/v1/users/?search={search}")
    assert response.status_code == 200, response.status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "search",
    ("Josh", "Ivan", "Dunin", "NotFoundValue"),
)
@timeit(duration=150)
def test_v2(user, search):
    response = user.get(f"/v2/users/?search={search}")
    assert response.status_code == 200, response.status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "search",
    ("Иван", "Сергеевич", "Иванова"),
)
@timeit(duration=150)
def test_v2_ru(user, search):
    response = user.get(f"/v2/users/?search={search}")
    assert response.status_code == 200, response.status_code


# @pytest.mark.django_db
# def test_v3(user):
#     """здесь теста нет, но поймать запросов и разобраться,
#     какие изменения в БД сделать, чтобы его улучшить"""
#     # response = user.get("/v3/users/", params={"search": "Иван"})
