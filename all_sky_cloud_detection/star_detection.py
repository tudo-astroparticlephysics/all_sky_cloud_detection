from skimage.feature import blob_log
import warnings


def find_stars(image, threshold, min_sigma=1, max_sigma=3, num_sigma=3):
    """This function finds bright blobs in an image using the Laplacian of Gaussion method.
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
            standard deviation of the Gaussian kernel that detected the blobs
    """
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore')
        blobs = blob_log(
            image,
            min_sigma=min_sigma,
            max_sigma=max_sigma,
            num_sigma=num_sigma,
            threshold=threshold,
        )
    row, column, size = blobs.T
    return row, column, size
