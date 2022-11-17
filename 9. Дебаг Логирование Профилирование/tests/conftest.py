from pathlib import Path
from uuid import UUID

import pytest

from app.stats import Top


@pytest.fixture
def prepare_top():

    def do_prepare(out: str):
        top = []
        for line in out.strip().split("\n"):
            uuid, value = line.strip().split("\t")
            top.append(Top(UUID(uuid), int(value)))
        return top

    return do_prepare


@pytest.fixture
def small_file():
    return Path(__file__).parent.parent / "small-data.tsv"


@pytest.fixture
def big_file():
    return Path(__file__).parent.parent / "data.tsv"
