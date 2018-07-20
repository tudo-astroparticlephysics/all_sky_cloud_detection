test_file = 'tests/resources/cta_images/starry.fits.gz'


def test_file():
    from all_sky_cloud_detection.io import read_file

    image, file_format = read_file(test_file)

    assert image.shape == (1699, 1699)
