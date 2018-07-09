import numpy as np
from all_sky_cloud_detection.coordinate_transformation import horizontal2pixel
from all_sky_cloud_detection.calculate_cloudiness import calculate_cloudiness
from all_sky_cloud_detection.time import get_time
from all_sky_cloud_detection.catalog import read_catalog, transform_catalog, match_catalogs
from all_sky_cloud_detection.star_selection import limit_zenith_angle
from all_sky_cloud_detection.find_blobs import find_blobs
from all_sky_cloud_detection.camera_classes import iceact, cta
from all_sky_cloud_detection.io import read_fits
from all_sky_cloud_detection.preparation import normalize_image
from all_sky_cloud_detection.plotting import plot_image


def process_image(path, file_format, cam):
    """
    This function processes an image and returns a cloudiness parameter,
    the time the image was taken and the average pixel brightness.
    Parameters
    -----------
    path: str
        path to the image to be analyzed
    file_format: str
        file format of the images
    cam: camclass object
        camera

    Returns
    -------
    cloudiness: float
        Cloudiness of the analyzed images
    time: astropy.Time
        Timestamp of the images
    mean: float
        mean pixel brightness
    """

    catalog = read_catalog(max_magnitude=cam.mag)
    ra_catalog = catalog['ra']
    dec_catalog = catalog['dec']

    imagess = read_fits(path)
    imagess = normalize_image(imagess, scale=2**16)
    imagess[np.isnan(imagess)] = np.nanmin(imagess)

    mean = np.mean(imagess)

    row, col, size = find_blobs(path, file_format, cam.image.threshold)
    time = get_time(path, cam)
    image_catalog = limit_zenith_angle(row, col, cam, 20, time)

    limited_row, limited_col= horizontal2pixel(image_catalog.alt, image_catalog.az, cam)

    if not image_catalog:
        cloudiness = 1.0
    else:
        image_row, image_col = horizontal2pixel(image_catalog.alt, image_catalog.az, cam)
        catalog = transform_catalog(ra_catalog, dec_catalog, time, cam)
        image_matches, catalog_matches, matches = match_catalogs(catalog, image_catalog, cam, time)
        cloudiness = calculate_cloudiness(cam, catalog, matches, 20, time)
        plot_image(path, cam, image_matches, limited_row[0], limited_col[0])

    return cloudiness, time, mean
