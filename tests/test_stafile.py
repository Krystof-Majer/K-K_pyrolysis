from pytest import fixture

from PyroPara.stafile import STAfile


@fixture
def sta_file():
    file = STAfile()
    file.load_data("tests/fixtures/data.txt")

    return file


def test_is_loaded(sta_file):
    assert sta_file._df is not None
