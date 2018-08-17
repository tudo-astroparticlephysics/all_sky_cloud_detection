from all_sky_cloud_detection.coordinate_transformation import horizontal2pixel
import numpy as np
from all_sky_cloud_detection.star_selection import limit_zenith_angle_catalog


def calculate_cloudiness(cam, catalog, angle, time, matches_magnitude, magnitude):
    """
    This function calculates the cloudiness of an image.
    Parameters
    -----------
    cam: camclass object
        camera
    catalog: Array
        Star catalog
    matches: float
    Number of stars from the catalog that match the stars in the image
    Returns
    -------
    cloudiness: float
        Cloudiness of the analyzed image
    """
    catalog_row, catalog_col = horizontal2pixel(catalog.alt, catalog.az, cam)

    limited_catalog, mag = limit_zenith_angle_catalog(catalog_row[0], catalog_col[0], cam, angle, time, magnitude)
    limited_catalog_row, limited_catalog_col = horizontal2pixel(limited_catalog.alt, limited_catalog.az, cam)
    visible_stars = np.sum(2.5**(matches_magnitude))
    all_stars = np.sum(2.5**(mag))
    cloudiness = np.round(1 - visible_stars / all_stars, 2)

    return cloudiness, limited_catalog_row[0], limited_catalog_col[0]
