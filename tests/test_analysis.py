import pytest

from PyroPara.analysis import Analysis


@pytest.fixture
def analysis():
    return Analysis()
