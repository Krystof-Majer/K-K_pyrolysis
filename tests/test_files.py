from pytest import fixture, raises

from PyroPara.files import TemperatureFile


@fixture
def temperature_file():
    file = TemperatureFile()
    file.load("tests/fixtures/data.txt")

    return file


def test_temperature_file_not_loaded():
    file = TemperatureFile()

    with raises(TypeError):
        file.rows
