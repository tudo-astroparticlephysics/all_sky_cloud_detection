from astropy.time import Time
from astropy.io import fits
import scipy.io as sio


def get_time(image, file_type):
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
    if file_type == 'fits':
        image = fits.open(image)
        timestamp = image[0].header['DATE-OBS']
        time = Time(timestamp, scale='utc')
        return time
    if file_type == 'mat':
        timestamp = sio.loadmat('../tests/resources/CTA_Images/matlab/CTA_AllSkyCam_2016-01-01_19-43-30.mat')['UTC1']
        date, time = timestamp[0].split(' ')
        date = date.replace('/', '-')
        time = Time(date+str('T')+time, scale='utc')
        return time
