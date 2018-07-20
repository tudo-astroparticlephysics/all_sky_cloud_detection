test_file = 'tests/resources/CTA_AllSkyCam_2015-12-22_03-35-55_1.fits.gz'


def test_find_stars():
    from all_sky_cloud_detection.io import read_file
    from all_sky_cloud_detection.star_detection import find_stars
    from all_sky_cloud_detection.preparation import normalize_image

    image, file_type = read_file(test_file)
    image = normalize_image(image, scale=2**16)

    row, column, size = find_stars(image, threshold=0.005)
    assert 500 < len(size) < 2000, 'did not find as many stars as expected'
    print(len(size))
