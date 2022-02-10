import pytest

from PyroPara.analysis import get_beta
from PyroPara.filter import FILTERS
from PyroPara.stafile import STAfile

PATH = "tests/fixtures/PYRO_MDF_30_700_N2_50_Kmin_recal_02.txt"


@pytest.fixture
def sta_file():
    beta = get_beta(PATH)
    file = STAfile(path=PATH, beta=beta, filter=FILTERS[50])
    file.load()

    return file


def test_is_loaded(sta_file):
    assert sta_file._df is not None


def test_is_complete(sta_file):
    assert len(sta_file._df.columns) == 7


def test_is_symmetrical(sta_file):
    assert len(sta_file._df.temperature) == len(sta_file._df.mass)


def test_valid_beta(sta_file):
    assert sta_file.beta > 0


def test_rows(sta_file):
    pass
