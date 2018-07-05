

def test_cloudy():
    from all_sky_cloud_detection.process_image import process_image
    from all_sky_cloud_detection.camera_classes import iceact

    cl, time, mean_brightness = process_image('tests/resources/iceact_images/cloudy.fits', 'fits', iceact)

    assert cl > 0.75

def test_starry():
    from all_sky_cloud_detection.process_image import process_image
    from all_sky_cloud_detection.camera_classes import iceact

    cl, time, mean_brightness = process_image('tests/resources/iceact_images/starry.fits', 'fits', iceact)

    assert cl < 0.2
