from astropy.coordinates import solar_system_ephemeris, SkyCoord, AltAz, Angle
from all_sky_cloud_detection.coordinate_transformation import horizontal2pixel
import numpy as np
from astropy.coordinates import get_body


def moon_coordinates(time, cam):
    """This function searches for the moon position at a given time.

    Parameters
    -----------
    time: 'astropy.time.core.Time'
        Time the image was taken.
    cam: 'str'
        Camera
    Returns
    -------
    moon_altitude:  'float'
        Altitude of the moon at the time the image was taken [radians]
    """
    observer = cam.location
    object = 'moon'
    with solar_system_ephemeris.set('builtin'):
        coordinates = get_body(object, time, observer)

    ra = coordinates.ra
    dec = coordinates.dec
    moon_position = SkyCoord(ra=ra, dec=dec, frame='icrs', unit='deg')
    moon_position_altaz = moon_position.transform_to(AltAz(obstime=time, location=observer))
    moon_altitude = moon_position_altaz.alt.radian
    print('time', type(time))
    return moon_altitude


def sun_coordinates(time, cam):
    """This function searches for the sun position at a given time.

    Parameters
    -----------
    time: 'astropy.time.core.Time'
        Time the image was taken.
    cam: 'str'
        Camera
    Returns
    -------
    sun_altitude:  'float'
        Altitude of the sun at the time the image was taken [radians]
    """
    observer = cam.location
    object = 'sun'
    with solar_system_ephemeris.set('builtin'):
        coordinates = get_body(object, time, observer)

    ra = coordinates.ra
    dec = coordinates.dec
    sun_position = SkyCoord(ra=ra, dec=dec, frame='icrs', unit='deg')
    sun_position_altaz = sun_position.transform_to(AltAz(obstime=time, location=observer))
    sun_altitude = sun_position_altaz.alt.radian

    return sun_altitude


def celestial_objects(time, cam):
    """This function searches for positions of celestial objects at a given time
    Parameters
    -----------
    time: astropy SkyCoord time object
            Time from the fits header of the image
    cam: string
        Camera name
    Returns
    -------
    row: Array
        Pixel coordinates of celestial objects on the y axis
    col: Array
        Pixel coordinates of celestial objects on the x axis
    """
    pos_altaz = moon_coordinates(time, cam)
    row, col = horizontal2pixel(pos_altaz.alt, pos_altaz.az, cam)
    row, col = row[0], col[0]
    size = np.ones(len(row))
    return row, col, size


def crop_moon(time, cam, image_stars, catalog_stars):
    moon_position = moon_coordinates(time, cam)
    idx_img, idx_moon1, d2d, d3d = moon_position.search_around_sky(image_stars, Angle('15d'))
    idx_cat, idx_moon2, d2d, d3d = moon_position.search_around_sky(catalog_stars, Angle('15d'))
    image_stars = image_stars[~idx_img]
    catalog_stars = catalog_stars[~idx_cat]
    return image_stars, catalog_stars
