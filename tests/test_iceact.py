import astropy.units as u


def test_images():
    from all_sky_cloud_detection.cameras import iceact as cam
    from all_sky_cloud_detection.catalog import read_catalog, transform_catalog
    from all_sky_cloud_detection.star_detection import find_stars, find_matching_stars
    from all_sky_cloud_detection.calculate_cloudiness import calculate_cloudiness_simple

    images = [
        'tests/resources/iceact_images/cloudy.fits',
        'tests/resources/iceact_images/starry.fits',
    ]

    limits = [
        (0.5, 1),
        (0.0, 0.5),
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
