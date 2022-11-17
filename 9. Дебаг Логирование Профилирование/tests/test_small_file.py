from datetime import date

from app.stats import calculate_top


def test_top_5_shows(small_file, prepare_top):
    top = calculate_top(
        small_file,
        date(2020, 1, 1),
        date(2020, 2, 1),
        "shows",
        5,
    )
    assert len(top) == 5
    assert top == prepare_top("""
        8bf64597-ffe5-468e-9af4-d538f6d841ec	845641
        f744f709-98fe-449a-aab1-d8d1bfa4a38d	815117
        b605eb9d-6110-475d-9396-8758a58234e8	804740
        85f762a9-c1ab-4dd6-b01b-f49a65065788	804134
        acab183d-7b5e-4975-954a-6518df026ec4	803163
    """)


def test_test_top_20_clicks(small_file, prepare_top):
    top = calculate_top(
        small_file,
        date(2020, 1, 1),
        date(2020, 2, 1),
        "clicks",
        20,
    )
    assert len(top) == 10
    assert top == prepare_top("""
        85f762a9-c1ab-4dd6-b01b-f49a65065788	429619
        b605eb9d-6110-475d-9396-8758a58234e8	418610
        8bf64597-ffe5-468e-9af4-d538f6d841ec	416515
        9076f20d-bfe6-4374-a17f-0dae61a323cf	412813
        f744f709-98fe-449a-aab1-d8d1bfa4a38d	406898
        acab183d-7b5e-4975-954a-6518df026ec4	388007
        1e216c51-2034-4899-b56c-0860be526e27	381961
        325ddb8b-50ce-4666-a90b-0268fbb422f5	363302
        2c17082e-222f-47c0-aecd-a3a49d7c9de9	362285
        13014d73-c4aa-4f72-bd4c-3fd7b028789e	362159
    """)
