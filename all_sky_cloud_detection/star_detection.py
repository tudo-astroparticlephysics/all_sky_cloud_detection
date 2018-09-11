from skimage.feature import blob_log
from astropy.coordinates import match_coordinates_sky
import astropy.units as u
import warnings


def find_stars(
    image,
    threshold,
    min_sigma=1.0,
    max_sigma=3.0,
    num_sigma=4,
    log_scale=False,
):
    '''
    This function finds bright blobs in an image
    using the Laplacian of Gaussion method.

    Parameters
    -----------
    image: array
       The image, should have been normalized and invalid regions changed to black.
    threshold: float
       Determines wheter more or less bright blobs are found

    Returns
    -------
    row: array
        pixel positions of found blobs
    col: array
        pixel positions of found blobs
    size: array
        standard deviation of the Gaussian kernel that detected the blobs
    '''
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore')
        blobs = blob_log(
            image,
            min_sigma=min_sigma,
            max_sigma=max_sigma,
            num_sigma=num_sigma,
            threshold=threshold,
            log_scale=log_scale,
            overlap=0.0,
        )
    row, column, size = blobs.T
    return row, column, size


@u.quantity_input(max_sep=u.deg)
def find_matching_stars(catalog_stars, image_stars, max_sep=0.5 * u.deg):
    """This function compares star positions.
    Parameters
    -----------
    catalog_stars: SkyCoord(frame='altaz')
        Stars from a catalog.
    image_stars: SkyCoord(frame='altaz')
        Found blobs converted to altaz frame
    max_sep: astropy.units.Quantity[deg]
        maximum angular separation for the matches
    Returns
    -------
    matches: array
        indices of the blobs that where matched to a catalog star
    mask: array[bool]
        True where a star could be matched to a blob
    """
    idx, d2d, d3d = match_coordinates_sky(catalog_stars, image_stars)
    mask = d2d < max_sep

    return idx[mask], mask
