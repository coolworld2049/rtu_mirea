import pathlib

from pr2_cross_correlation.adviser.__main__ import Adviser

PRODUCT = "artist"


def test_pairs(adviser: Adviser):
    part_path = pathlib.Path(f"/user/{adviser.username}/output/pairs/part-00000")
    assert adviser.advise(part_path, PRODUCT, 5)


def test_stripes(adviser: Adviser):
    part_path = pathlib.Path(f"/user/{adviser.username}/output/stripes/part-00000")
    assert adviser.advise(part_path, PRODUCT, 5)
