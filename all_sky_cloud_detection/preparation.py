from skimage import img_as_float


def normalize_image(image, scale=1.0):
    image = img_as_float(image)
    return image / scale
