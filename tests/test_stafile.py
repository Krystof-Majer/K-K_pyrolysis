import pytest

from PyroPara.filter import FILTERS
from PyroPara.stafile import STAfile


@pytest.fixture
def sta_file():
    file = STAfile(
        "tests/fixtures/PYRO_MDF_30_700_N2_50_Kmin_recal_02.txt", FILTERS[50]
    )
    file.load()

    return file


def test_is_loaded(sta_file):
    assert sta_file._df is not None


def test_is_complete(sta_file):
    assert len(sta_file._df.columns) == 7


def test_is_symmetrical(sta_file):
    assert len(sta_file._df.temperature) == len(sta_file._df.mass)


# def test_valid_beta(sta_file):  # TODO: test beta property
#    assert sta_file._beta > 0


def test_rows(sta_file):
    pass
