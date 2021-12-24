import pytest
from PyroPara.stafile import STAfile


@pytest.fixture
def sta_file():
    file = STAfile()
    file.load_data("tests/fixtures/data.txt")

    return file


def test_is_loaded(sta_file):
    assert sta_file._df is not None


def test_is_complete(sta_file):
    assert len(sta_file._df.columns) == 7


def test_is_symmetrical(sta_file):
    assert len(sta_file._df.temperature) == len(sta_file._df.mass)


def test_valid_beta(sta_file):  # TODO: test beta property
    assert sta_file._beta > 0
    pass


def test_rows(sta_file):
    pass
