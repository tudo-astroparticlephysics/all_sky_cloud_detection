from astropy.time import Time
from astropy.io import fits
import scipy.io as sio


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
    timestamps = cam.image.timestamp
    if file_type == '.fits' or file_type == '.gz':
        image = fits.open(image)
        for timestamp in timestamps:
            try:
                timestamp = image[0].header[timestamp]
                time = Time(timestamp, scale='utc')
                print('Wrong timestamp')
            except KeyError:
                continue

    if file_type == '.mat':
        for timestamp in timestamps:
            try:
                timestamp = sio.loadmat(image)[timestamp]
                date, time = timestamp[0].split(' ')
                date = date.replace('/', '-')
                time = Time(date+str('T')+time, scale='utc')
            except KeyError:
                print('Wrong timestamp')
                continue
    return time
