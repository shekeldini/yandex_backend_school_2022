from datetime import date

import pytest

from app.stats import calculate_top


@pytest.mark.timeout(2)
def test_top_10_shows_september_2020(big_file, prepare_top):
    top = calculate_top(
        big_file,
        date(2020, 9, 1),
        date(2020, 9, 30),
        "shows",
        10,
    )
    assert len(top) == 10
    assert top == prepare_top("""
        e1d8bd02-2b2a-4a07-856a-4de06b0b0d7d	12250758
        d6f9d10c-820b-4b85-b254-9e5b8102aa8a	12235653
        a8ec279a-b257-4794-8c2e-c8740396f087	12196391
        b4d40839-e584-4bd9-9820-f23d1511a45e	12166676
        d8911415-dd17-4baf-b993-94440c2f5036	12147414
        397ccaa5-7541-4ed4-86ba-18c38889cd56	12137991
        bfda9ce4-9a4a-4748-a8a1-57a47b5607d1	12136375
        03fde7a9-accd-4c3f-b874-311a015f0989	12125620
        d7d2733c-0b05-4fe0-8383-bfea28ed3140	12113426
        6e5246a9-593c-4eaf-b79c-8d397fbf6037	12109579
    """)
