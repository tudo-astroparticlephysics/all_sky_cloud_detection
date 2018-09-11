import numpy as np


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
    visible_stars = np.sum(2.5**magnitude[found])
    all_stars = np.sum(2.5**magnitude)
    cloudiness = 1 - visible_stars / all_stars

    return cloudiness


def calculate_cloudiness_simple(found):
    """
    This function calculates the cloudiness of an image.
    Cloudiness is simply the percentage of found stars
    Parameters
    -----------
    found: array
        Boolean array, true where a catalog star could be found in the image
    Returns
    -------
    cloudiness: float
        Cloudiness of the analyzed image
    """

    return 1 - np.mean(found)
