import numpy as np


def test_read():
    from all_sky_cloud_detection.catalog import read_catalog

    catalog = read_catalog()
    assert catalog.colnames == ['HIP', 'ra', 'dec', 'v_mag', 'variability']


def test_max_magnitude():
    from all_sky_cloud_detection.catalog import read_catalog

    catalog = read_catalog(max_magnitude=6)
    assert np.all(catalog['v_mag'] <= 6)

    catalog = read_catalog(max_magnitude=3)
    assert np.all(catalog['v_mag'] <= 3)

def test_max_variability():
    from all_sky_cloud_detection.catalog import read_catalog

    catalog = read_catalog(max_variability=2)
    assert np.any(catalog['variability'] >= 1)
    assert np.all(catalog['variability'] <= 2)
