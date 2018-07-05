import numpy as np
from all_sky_cloud_detection.coordinate_transformation import horizontal2pixel
from all_sky_cloud_detection.calculate_cloudiness import calculate_cloudiness
from all_sky_cloud_detection.time import get_time
from all_sky_cloud_detection.catalog import read_catalog, transform_catalog, match_catalogs
from all_sky_cloud_detection.zenith_angle import zenith_angle
from all_sky_cloud_detection.find_blobs import find_blobs

from all_sky_cloud_detection.io import read_fits
from all_sky_cloud_detection.preparation import normalize_image

def process_image(path, file_format, cam):
    """

    Parameters
    -----------
    path: str
        path to the image to be analyzed
    file_format: str
        file format of the images
    cam: Camera
        class of the all sky camera (camclass.cta or camclass.iceact)

    Returns
    -------
    cloudiness: float
        Cloudiness of the analyzed images
    time: astropy.Time
        Timestamp of the images
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
    image_catalog = zenith_angle(row, col, cam, 20, time)

    if not image_catalog:
        cloudiness = 1.0
    else:
        image_row, image_col = horizontal2pixel(image_catalog.alt, image_catalog.az, cam)
        catalog = transform_catalog(ra_catalog, dec_catalog, time, cam)
        c_matches, catalog_matches, matches = match_catalogs(catalog, image_catalog, cam, time)
        cloudiness = calculate_cloudiness(cam, catalog, matches)
    return cloudiness, time, mean
