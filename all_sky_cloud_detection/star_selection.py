import astropy.units as u
from astropy.coordinates import Angle
from all_sky_cloud_detection.coordinate_transformation import pixel2horizontal
from astropy.coordinates import SkyCoord
import numpy as np
from all_sky_cloud_detection.preparation import normalize_image

def limit_zenith_angle(row, col, cam, angle, time):
    """This function limits the zenith angle and thus the number of stars used
     in the calculation of cloud cover. If the angle is set to 20 degrees,
     the stars used in the calculation are in a zenith angle range of 0 to 80
     degrees.
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
    r, phi, theta = pixel2horizontal(row, col, cam)

    angle = Angle(angle*u.deg)
    mask = theta > angle
    theta_new = theta[mask]
    phi_new = phi[mask]

    c = SkyCoord(
        az=phi_new,
        alt=theta_new,
        frame='altaz',
        obstime=time,
        location=observer
        )
    return c

def limit_zenith_angle_catalog(row, col, cam, angle, time, magnitude):
    """This function limits the zenith angle and thus the number of stars used
     in the calculation of cloud cover. If the angle is set to 20 degrees,
     the stars used in the calculation are in a zenith angle range of 0 to 80
     degrees.
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
    r, phi, theta = pixel2horizontal(row, col, cam)

    angle = Angle(angle*u.deg)
    mask = theta > angle
    theta_new = theta[mask]
    phi_new = phi[mask]
    mag = magnitude[mask]
    c = SkyCoord(
        az=phi_new,
        alt=theta_new,
        frame='altaz',
        obstime=time,
        location=observer
        )
    return c, mag


def delete_big_blobs(row, col, size):
    mask = size < 20
    new_row = row[mask]
    new_col = col[mask]
    new_size = size[mask]
    number_big_blobs = len(size)-len(new_size)
    return new_row, new_col, new_size, number_big_blobs


def mean_pixel_brightness(image, file_type):
    image = normalize_image(image, scale=2**16)
    image[np.isnan(image)] = np.nanmin(image)
    mean = np.mean(image)
    return mean
