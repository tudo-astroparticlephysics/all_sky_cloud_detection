# coding: utf-8
from all_sky_cloud_detection.io import read_fits, read_matlab
from all_sky_cloud_detection.preparation import normalize_image
from all_sky_cloud_detection.star_detection import find_stars


def find_blobs(img_name, file_type, threshold, overlap):
    """This function searches for bright blobs above the threshold in an image.

    Parameters
     -----------
    img_name : string
        Name of the processed image.
    format : string
        Format of the image.
    threshold : float
        Reduce this to detect blobs with less intensities.

    Returns
    -------
    row : array
        y coordinates of found blobs in pixels
    col : array
        x coordinates of found blobs in pixles
    size: array
        Standard deviation of the Gaussian kernel which detected the blob.
    image: pdf file
        Image with blobs saved in same directory as the input file
    """

    if file_type == 'fits':
        scale = 2**16
        image = normalize_image(read_fits(img_name), scale=scale)
        row, col, size = find_stars(image, threshold=threshold, overlap=overlap)
        return row, col, size
    if file_type == 'mat':
        scale = 2**16
        image = normalize_image(read_matlab(img_name), scale=scale)
        row, col, size = find_stars(image, threshold=threshold, overlap=overlap)
        return row, col, size
    #improve else case when more file types are supported
    else:
        scale = 2**16
        image = normalize_image(read_fits(img_name), scale=scale)
        row, col, size = find_stars(image, threshold=threshold)
        return row, col, size
