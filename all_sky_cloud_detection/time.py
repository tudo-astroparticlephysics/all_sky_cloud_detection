from astropy.time import Time
from astropy.io import fits
import scipy.io as sio
from all_sky_cloud_detection.camera_classes import cta


def get_time(image, cam, file_type):
    """Get the timestamp of the analyzed image.

    Parameters
    -----------
    path: 'str'
        Path to the image to be analyzed
    cam: 'str'
        Camera
    file_type: 'str'
        File format of the analyzed image
    Returns
    -------
    time: astropy.time.core.Time'
        Timestamp of the given image
    """
    timestamps = cam.image.timestamp
    if file_type == '.fits' or file_type == '.gz':
        image = fits.open(image)
        for timestamp in timestamps:
            try:
                timestamp = image[0].header[timestamp]
                time = Time(timestamp, scale='utc')
            except KeyError:
                continue

    if file_type == '.mat':
        for timestamp in timestamps:
            try:
                timestamp = sio.loadmat(image)[timestamp]
                if cam == cta:
                    date, time = timestamp[0].split(' ')
                    date = date.replace('/', '-')
                    time = Time(date+str('T')+time, scale='utc')
            except KeyError:
                continue
    return time
