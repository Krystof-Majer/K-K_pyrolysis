import pandas as pd
import pytest

from PyroPara.analysis import get_beta
from PyroPara.filter import FILTERS
from PyroPara.stafile import STAfile

PATH_30 = "tests/fixtures/PYRO_MDF_30_900_N2_30Kmin_recal_02.txt"
PATH_30_PROCESSED = "tests/fixtures/processed_file_30K_MDF.txt"
PATH_30_LOCAL_MINIMA = "tests/fixtures/beta_30K_local_minima.txt"


@pytest.fixture
def sta_file():
    beta = get_beta(PATH_30)
    file = STAfile(path=PATH_30, beta=beta, filter=FILTERS[30])

    file.load()

    return file


@pytest.fixture
def sta_file_processed():
    file = pd.read_csv(PATH_30_PROCESSED, sep=",", encoding="cp1250")
    return file


@pytest.fixture
def sta_file_local_minima():
    pass


def test_is_loaded(sta_file):
    assert sta_file._df is not None


def test_is_complete(sta_file):
    assert len(sta_file._df.columns) == 7


def test_is_symmetrical(sta_file):
    assert len(sta_file._df.temperature) == len(sta_file._df.mass)


def test_valid_beta(sta_file):
    assert sta_file.beta == 30.0


def test_process(sta_file: STAfile, sta_file_processed):
    sta_file.process()
    assert sta_file._df is not None
    pd.testing.assert_frame_equal(
        sta_file._df, sta_file_processed, check_less_precise=True
    )


def test_local_minima():
    pass
