test_file = 'tests/resources/CTA_AllSkyCam_2016-01-04_23-39-11.mat_1.fits.gz'


def test_find_stars():
    from all_sky_cloud_detection.io import read_fits
    from all_sky_cloud_detection.star_detection import find_stars
    from all_sky_cloud_detection.preparation import normalize_image

    image = read_fits(test_file)
    image = normalize_image(image, scale=2**16)

    row, column, size = find_stars(image, threshold=0.005)
    assert 500 < len(size) < 2000, 'did not find as many stars as expected'
    print(len(size))
