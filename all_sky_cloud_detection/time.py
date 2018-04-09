import astropy.units as u
from astropy.time import Time
from astropy.coordinates import Angle
from astropy.io import fits
from all_sky_cloud_detection.coordinate_transformation import pixel2spherical
from astropy.coordinates import SkyCoord


def get_time(image):
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
    timestamp = image[0].header['DATE-OBS']
    time = Time(timestamp, scale='utc')
    return time


def zenith_angle(row, col, cam, angle, time):
    """This function cuts out bright blobs in an image at low zenith angles
    Parameters
    -----------
    row: array
        pixel positions, y axis
    col: array
        pixel positions, x axis
    cam: string
        name of the used all sky camera
    angle: float
            limitation of the zenith angle
    time: astropy timestamp
            timestamp of the used image

    Returns
    -------
    c: array of skycoord objects
        azimuth and altitude of the remaining bright blobs
    """
    observer = cam.location
    time = time
    r, phi, theta = pixel2spherical(row, col, cam.lens.r2theta, cam)
    angle = Angle(angle*u.deg)
    theta_new = theta[theta > (angle)]
    phi_new = phi[theta > (angle)]
    c = SkyCoord(
        az=phi_new,
        alt=theta_new,
        frame='altaz',
        obstime=time,
        location=observer
        )
    return c
