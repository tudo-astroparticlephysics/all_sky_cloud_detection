from astropy.coordinates import solar_system_ephemeris, SkyCoord, AltAz, Angle
from all_sky_cloud_detection.coordinate_transformation import horizontal2pixel
import numpy as np
from astropy.coordinates import get_body

def get_planets_altaz(time, cam):
    """This function searches for positions of celestial objects at a given time
    Parameters
    -----------
    time: astropy SkyCoord time object
            Time from the fits header of the image
    cam: string
        Camera name
    Returns
    -------
    pos_altaz: array
        Array of celestial objects in altaz
    """
    observer = cam.location
    with solar_system_ephemeris.set('builtin'):
        moon = get_body('moon', time, observer)
        sun = get_body('sun', time, observer)
        mercury = get_body('mercury', time, observer)
        venus = get_body('venus', time, observer)
        mars = get_body('mars', time, observer)
        jupiter = get_body('jupiter', time, observer)
        saturn = get_body('saturn', time, observer)
        uranus = get_body('uranus', time, observer)
        neptune = get_body('neptune', time, observer)

    ra_objects = [
        moon.ra,
        sun.ra,
        mercury.ra,
        venus.ra,
        mars.ra,
        jupiter.ra,
        saturn.ra,
        uranus.ra,
        neptune.ra]
    dec_objects = [
        moon.dec,
        sun.dec,
        mercury.dec,
        venus.dec,
        mars.dec,
        jupiter.dec,
        saturn.dec,
        uranus.dec,
        neptune.dec]
    pos = SkyCoord(ra=ra_objects, dec=dec_objects, frame='icrs', unit='deg')
    pos_altaz = pos.transform_to(AltAz(obstime=time, location=observer))
    return pos_altaz


def get_planets(time, cam):
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
    pos_altaz = get_planets_altaz(time, cam)
    row, col = horizontal2pixel(pos_altaz.alt, pos_altaz.az, cam)
    row, col = row[0], col[0]
    size = np.ones(len(row))
    return row, col, size


def crop_moon(time, cam, image_stars, catalog_stars):
    planets = get_planets_altaz(time, cam)
    moon_sun = planets[0:2]
    idx_img, idx_moon1, d2d, d3d = moon_sun.search_around_sky(image_stars, Angle('15d'))
    idx_cat, idx_moon2, d2d, d3d = moon_sun.search_around_sky(catalog_stars, Angle('15d'))
    image_stars = image_stars[~idx_img]
    catalog_stars = catalog_stars[~idx_cat]
    return image_stars, catalog_stars
