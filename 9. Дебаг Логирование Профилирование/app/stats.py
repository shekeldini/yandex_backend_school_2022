from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import NamedTuple
from uuid import UUID
from cProfile import Profile
import pstats


class Record(NamedTuple):
    day: date
    company: UUID
    region: int
    shows: int
    clicks: int


class Top(NamedTuple):
    company: UUID
    value: int


def bin_search(l: int, r: int, start_date: date, data: list) -> int:
    while l < r:
        m = (l + r) // 2
        day, company, region, shows, clicks = data[m].split("\t")
        day = date.fromisoformat(day)
        if day > start_date:
            r = m - 1
        elif day == start_date:
            r = m
        else:
            l = m + 1
    return l


def get_records(
        tsv_file: Path,
        start_date: date,
        end_date: date
):
    with tsv_file.open("r") as fp:
        # первая строка отвечает за название столбцов, пропустим ее
        next(fp)
        all_text: list = fp.readlines()
        # с помощью бинарного поиска найдем индекс начала start_date в файле
        first_index = bin_search(0, len(all_text), start_date, all_text)
        for i in range(first_index, len(all_text)):
            day, company, region, shows, clicks = all_text[i].split("\t")
            day = date.fromisoformat(day)

            # отсеем лишние записи
            if start_date <= day <= end_date:
                # чтобы не хранить все строки в памяти
                yield Record(
                    day,
                    company,
                    int(region),
                    int(shows),
                    int(clicks),
                )
            # остановим итерацию по файлу, так как дальше только не интересующие нас строки
            if day > end_date:
                break


def calculate_top(
        tsv_file_path: Path,
        start_date: date,
        end_date: date,
        stats_by: str,
        top_size: int
):
    companies = defaultdict(int)
    for record in get_records(tsv_file_path, start_date, end_date):
        companies[record.company] += getattr(record, stats_by)

    # заменил на базовую сортировку с использованием lambda функции, так как это более гибкий и понятный вариант

    companies_queue = sorted(
        companies.items(),
        key=lambda x: x[1],
        reverse=True
    )

    top_companies = []
    # если один из итераторов остановится, то дальше итерироваться не будем
    for _, item in zip(range(top_size), companies_queue):
        company, value = item
        top_companies.append(
            Top(
                UUID(company),
                value
            )
        )

    return top_companies
