import pytest

from PyroPara.analysis import Analysis

DIRECTORY = "tests/fixtures"


@pytest.fixture
def analysis():
    return Analysis()


def test_load_files(analysis):
    analysis.load_files(DIRECTORY)
    assert len(analysis) == 4


def test_run(analysis):
    pass
