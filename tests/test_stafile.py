from pytest import fixture, raises

from PyroPara.stafile import STAfile


@fixture
def STAfile():
    file = STAfile()
    file.load("tests/fixtures/data.txt")

    return file
