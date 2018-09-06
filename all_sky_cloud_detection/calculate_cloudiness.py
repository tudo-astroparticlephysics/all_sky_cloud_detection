from all_sky_cloud_detection.coordinate_transformation import horizontal2pixel
import numpy as np
from all_sky_cloud_detection.star_selection import limit_zenith_angle_catalog


def calculate_cloudiness_weighted(magnitude, found):
    """
    This function calculates the cloudiness of an image.
    Parameters
    -----------
    magnitude: array
        visual magnitude of the stars
    Number of stars from the catalog that match the stars in the image
    Returns
    -------
    cloudiness: float
        Cloudiness of the analyzed image
    """
    visible_stars = np.sum(2.5**(magnitude[found]))
    all_stars = np.sum(2.5**(mag))
    cloudiness = 1- visible_stars/all_stars

    return cloudiness, limited_catalog_row[0], limited_catalog_col[0]


def calculate_cloudiness_simple(found):
    """
    This function calculates the cloudiness of an image.
    Cloudiness is simply the percentage of found stars

    Parameters
    -----------
    magnitude: array
        visual magnitude of the stars
    Number of stars from the catalog that match the stars in the image
    Returns
    -------
    cloudiness: float
        Cloudiness of the analyzed image
    """

    return np.mean(found)
