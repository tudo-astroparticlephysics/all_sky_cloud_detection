from astropy.time import Time
from astropy.io import fits
import scipy.io as sio
from all_sky_cloud_detection.camera_classes import iceact, cta


def get_time(image, cam, file_type):
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
    if cam == cta:
        if file_type == '.fits' or file_type == '.gz':
            #hier mit io funktion verkürzen
            image = fits.open(image)
            timestamp = image[0].header['TIMEUTC']
            time = Time(timestamp, scale='utc')
            if file_type == '.mat':
                timestamp = sio.loadmat(image)['UTC1']
                date, time = timestamp[0].split(' ')
                date = date.replace('/', '-')
                time = Time(date+str('T')+time, scale='utc')
        if cam == iceact:
            if file_type == '.fits' or file_type == '.gz':
                #hier mit io funktion verkürzen
                image = fits.open(image)
                timestamp = image[0].header['DATE-OBS']
                time = Time(timestamp, scale='utc')
    return time
