import pytest

from pr2_cross_correlation.adviser.__main__ import Adviser


@pytest.fixture()
def adviser():
    username = "ivanovnp"
    adviser = Adviser(
        host="localhost",
        port=50070,
        username=username,
    )
    return adviser
