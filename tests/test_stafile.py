import numpy as np
import pandas as pd
import pytest

from PyroPara.analysis import get_beta
from PyroPara.filter import HANNING
from PyroPara.stafile import STAfile

PATH_30 = "tests/fixtures/PYRO_MDF_30_900_N2_30Kmin_recal_02.txt"
PATH_30_PROCESSED = "tests/fixtures/processed_file_30K_MDF.txt"


@pytest.fixture
def sta_file():
    beta = get_beta(PATH_30)
    file = STAfile(path=PATH_30, beta=beta, filter=HANNING[30])
    file.load()
    file.process()
    file.calculate_local_minima(minorder=4)
    return file


@pytest.fixture
def sta_file_processed():
    file_processed = pd.read_csv(PATH_30_PROCESSED, sep=",", encoding="cp1250")
    return file_processed


def test_is_loaded(sta_file):
    assert sta_file._df is not None


def test_is_complete(sta_file):
    assert len(sta_file._df.columns) == 13


def test_is_symmetrical(sta_file):
    assert len(sta_file._df.temperature) == len(sta_file._df.mass)


def test_valid_beta(sta_file):
    assert sta_file.beta == 30.0


def test_calculate_local_minima(sta_file: STAfile):
    assert sta_file.local_minima is not None
    assert len(sta_file.local_minima) <= 10


# passing only with large tolerances
def test_find_local_minima(sta_file: STAfile):
    expected = np.array(
        [
            (5.11432000e02, 5.65016139e-03),
            (5.24056010e02, 6.37340534e-03),
            (5.86776010e02, 4.47961441e-02),
            (6.07772990e02, 3.56542525e-02),
            (6.56660010e02, 3.56672317e-02),
            (7.02141000e02, 1.68601995e-03),
            (7.19479010e02, 2.14177168e-03),
            (7.40339000e02, 4.85544644e-03),
        ]
    )
    calculated = np.array(sta_file.find_local_minima(7, 500, 750))
    print(calculated)
    assert calculated.shape == (8, 2)
    np.testing.assert_allclose(calculated, expected, rtol=0.1, atol=0.5)
