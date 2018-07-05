def test_read():
    from all_sky_cloud_detection.catalog import read_catalog

    catalog = read_catalog()

    assert len(catalog) == 118218
    assert catalog.colnames == ['HIP', 'ra', 'dec', 'v_mag', 'variability']


def test_max_magnitude():
    from all_sky_cloud_detection.catalog import read_catalog

    catalog = read_catalog(max_magnitude=8)

    assert len(catalog) == 2895
