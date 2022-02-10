from click import get_binary_stream
import pytest

from PyroPara.stafile import STAfile
from PyroPara.analysis import get_beta
from PyroPara.filter import FILTERS

PATH = "tests/fixtures/PYRO_MDF_30_900_N2_30Kmin_recal_02.txt"


@pytest.fixture
def sta_file():
    beta = get_beta(PATH)
    file = STAfile(path=PATH, beta=beta, filter=FILTERS[30])

    file.load()

    return file


def test_is_loaded(sta_file):
    assert sta_file._df is not None


def test_is_complete(sta_file):
    assert len(sta_file._df.columns) == 7


def test_is_symmetrical(sta_file):
    assert len(sta_file._df.temperature) == len(sta_file._df.mass)


def test_valid_beta(sta_file):
    assert type(sta_file.beta) is float
    assert sta_file.beta > 0
