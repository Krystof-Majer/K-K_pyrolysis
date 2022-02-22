import pytest

from PyroPara.analysis import Analysis

DIRECTORY = "tests/fixtures"
PATH = "tests/fixtures/PYRO_MDF_30_900_N2_30Kmin_recal_02.txt"


@pytest.fixture
def analysis():
    return Analysis()


def test_load_all_files(analysis):
    analysis.load_all_files(DIRECTORY)
    assert len(analysis) == 3


def test_load_file(analysis):
    analysis.load_file(PATH)
    assert len(analysis) == 1
