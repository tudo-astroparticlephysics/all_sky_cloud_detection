from astropy.time import Time
from astropy.io import fits

def get_time(image, cam):
    """This function gives the timestamp embedded in the fits header
    Parameters
    -----------
    image: path
            path of the image
    Returns
    -------
    time: astropy timestamp
            timestamp of the given image
    """
    #header time angeben für verschiedene ka meras in klassen
    image = fits.open(image)
    timestamp = image[0].header[cam.image.timestamp]
    time = Time(timestamp, scale='utc')
    return time
