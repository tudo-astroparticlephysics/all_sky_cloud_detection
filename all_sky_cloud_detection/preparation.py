from skimage import img_as_float


def normalize_image(image, scale=1.0):
    """This function normalizes an image.
    Parameters
    -----------
    image: path
            Path where the image is located
    scale: float
            Parameter, depending on the image
    Returns
    -------
    array
    Normalized image
    """
    image = img_as_float(image)
    return image / scale
