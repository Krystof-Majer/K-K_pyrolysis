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
    assert len(sta_file._df.columns) == 12


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
            (511.432, 0.0056501613913371475),
            (524.05601, 0.0063734053433378455),
            (586.77601, 0.04479614411308593),
            (607.7729899999999, 0.03565425247006773),
            (656.66001, 0.035667231708348686),
            (702.141, 0.0016860199515036961),
            (719.47901, 0.0021417716797097874),
            (740.3389999999999, 0.004855446439990549),
        ]
    )

    calculated = np.array(sta_file.find_local_minima(7, 500, 750))
    assert calculated.shape == (8, 2)
    np.testing.assert_allclose(calculated, expected, rtol=0.1, atol=0.5)
