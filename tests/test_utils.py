from PyroPara.utils import get_beta


def test_get_beta():
    assert (
        get_beta("tests/fixtures/PYRO_MDF_30_700_N2_50_Kmin_recal_02.txt")
    ) == 50.0
    assert (
        get_beta("tests/fixtures/PYRO_MDF_30_900_N2_05Kmin_recal_02.txt")
    ) == 5.0
    assert (
        get_beta("tests/fixtures/PYRO_MDF_30_900_N2_30Kmin_recal_02.txt")
    ) == 30.0
