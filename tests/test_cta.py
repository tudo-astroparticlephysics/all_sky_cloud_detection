

def test_cloudy():
    from all_sky_cloud_detection.process_image import process_image
    from all_sky_cloud_detection.camera_classes import cta

    cl, time, mean_brightness, moon_altitude = process_image('tests/resources/cta_images/cloudy.fits.gz', cta)

    assert cl > 0.75

def test_starry():
    from all_sky_cloud_detection.process_image import process_image
    from all_sky_cloud_detection.camera_classes import cta

    cl, time, mean_brightness, moon_altitude = process_image('tests/resources/cta_images/starry.fits.gz', cta)

    assert cl < 0.2


def test_starry():
    from all_sky_cloud_detection.process_image import process_image
    from all_sky_cloud_detection.camera_classes import cta

    cl, time, mean_brightness, moon_altitude = process_image('tests/resources/cta_images/partly_cloudy.fits.gz', cta)

    assert cl > 0.25 and cl < 0.75
