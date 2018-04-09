from skimage.feature import blob_log
import warnings


def find_stars(image, threshold):
    """This function finds bright blobs in an image above a given threshold.
    Parameters
    -----------
    image: array
            Image, normalized with the normalize_image() function
    threshold: float
                Determines wheter more or less bright blobs are found
    Returns
    -------
    row: array
        pixel positions of found blobs (y axis)
    col: array
        pixel postions of found blobs (x axis)
    size: array
            size of the found blobs in pixels
    """
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore')
        blobs = blob_log(
            image,
            min_sigma=1,
            max_sigma=3,
            num_sigma=3,
            threshold=threshold,
        )
    row, column, size = blobs.T
    return row, column, size
