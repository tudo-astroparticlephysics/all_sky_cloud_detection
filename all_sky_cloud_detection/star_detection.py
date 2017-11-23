from skimage.feature import blob_log
import warnings


def find_stars(image, threshold):
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
