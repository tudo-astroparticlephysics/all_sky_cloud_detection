test_file = 'tests/resources/CTA_AllSkyCam_2016-01-04_23-39-11.mat_1.fits.gz'


def test_fits():
    from all_sky_cloud_detection.io import read_fits

    image = read_fits(test_file)

    assert image.shape == (1699, 1699)
