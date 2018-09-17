import numpy as np
import astropy.units as u


def test_read_fits():
    from all_sky_cloud_detection.cameras import cta_la_palma

    img = cta_la_palma.read('tests/resources/cta_images/starry.fits.gz')

    assert img.data.shape == (1699, 1699)
    assert np.all(img.data >= 0)
    assert np.all(img.data <= 1)


def test_images():
    from all_sky_cloud_detection.cameras import cta_la_palma as cam
    from all_sky_cloud_detection.catalog import read_catalog, transform_catalog
    from all_sky_cloud_detection.star_detection import find_stars, find_matching_stars
    from all_sky_cloud_detection.calculate_cloudiness import calculate_cloudiness_simple

    images = [
        'tests/resources/cta_images/starry_nomoon.fits.gz',
        'tests/resources/cta_images/starry.fits.gz',
        'tests/resources/cta_images/partly_cloudy.fits.gz',
        'tests/resources/cta_images/cloudy.fits.gz',
    ]

    limits = [
        (0, 0.1),
        (0, 0.2),
        (0.3, 0.7),
        (0.9, 1.0),
    ]

    catalog = read_catalog(
        max_magnitude=cam.max_magnitude,
        max_variability=None,
    )

    for (a, b), path in zip(limits, images):
        img = cam.read(path)

        # create catalog of possibly visible stars and planets
        stars_catalog, magnitude = transform_catalog(
            catalog, img.timestamp, cam, min_altitude=20,
        )

        r, c, s = find_stars(img.data, threshold=cam.threshold)
        found_altaz = cam.pixel2horizontal(r, c, img.timestamp)
        mask = found_altaz.alt.deg > 20

        idx, found = find_matching_stars(
            stars_catalog, found_altaz[mask], max_sep=0.25 * u.deg
        )

        cl = calculate_cloudiness_simple(found)

        assert a <= cl <= b
