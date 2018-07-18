from astropy.coordinates import solar_system_ephemeris, SkyCoord, AltAz, Angle
from all_sky_cloud_detection.coordinate_transformation import horizontal2pixel
import numpy as np
from astropy.coordinates import get_body

def moon_coordinates(time, cam):
    """This function searches for positions of celestial objects at a given time
    Parameters
    -----------
    time: astropy SkyCoord time object
            Time from the fits header of the image
    cam: camclass object
        Camera name
    Returns
    -------
    pos_altaz: array
        Array of celestial objects in altaz
    """
    observer = cam.location
    names = 'moon'#['moon', 'sun', 'mercury', 'venus', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune']
    with solar_system_ephemeris.set('builtin'):
        coordinates = get_body(names, time, observer)

    ra_objects = [coordinates.ra]
    dec_objects = [coordinates.dec]
    pos = SkyCoord(ra=ra_objects, dec=dec_objects, frame='icrs', unit='deg')
    pos_altaz = pos.transform_to(AltAz(obstime=time, location=observer))
    alt = pos_altaz.alt
    az = pos_altaz.az
    return alt, az


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
    pos_altaz = celestial_objects_altaz(time, cam)
    row, col = horizontal2pixel(pos_altaz.alt, pos_altaz.az, cam)
    row, col = row[0], col[0]
    size = np.ones(len(row))
    return row, col, size


def crop_moon(time, cam, image_stars, catalog_stars):
    planets = celestial_objects_altaz(time, cam)
    moon_sun = planets[0:2]
    idx_img, idx_moon1, d2d, d3d = moon_sun.search_around_sky(image_stars, Angle('15d'))
    idx_cat, idx_moon2, d2d, d3d = moon_sun.search_around_sky(catalog_stars, Angle('15d'))
    image_stars = image_stars[~idx_img]
    catalog_stars = catalog_stars[~idx_cat]
    return image_stars, catalog_stars
