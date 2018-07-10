from all_sky_cloud_detection.coordinate_transformation import horizontal2pixel
import numpy as np
from all_sky_cloud_detection.star_selection import limit_zenith_angle


def calculate_cloudiness(cam, catalog, matches, angle, time):
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
    row, col = horizontal2pixel(catalog.alt, catalog.az, cam)

    limited_catalog = limit_zenith_angle(row[0], col[0], cam, angle, time)
    limited_row, limited_col = horizontal2pixel(limited_catalog.alt, limited_catalog.az, cam)
    cloudiness = np.round(1-matches/len(limited_col), 2)
    return cloudiness
