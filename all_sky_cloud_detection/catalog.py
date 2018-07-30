from astropy.coordinates import SkyCoord, AltAz, Angle
import numpy as np
from all_sky_cloud_detection.coordinate_transformation import horizontal2pixel
from astropy.table import Table
from pkg_resources import resource_filename


catalog_path = resource_filename('all_sky_cloud_detection', 'resources/hipparcos.fits.gz')


def read_catalog(max_magnitude=None):
    """This function reads in star catalogs saved as csv file.
    Parameters
    -----------
    path: string
            Path of the catalog
    Returns
    -------
    catalog: astropy table object
            star catalog
    """
    catalog = Table.read(catalog_path)
    if max_magnitude is not None:
        catalog = catalog[catalog['variability'] == 1]
        catalog = catalog[catalog['v_mag'] <= max_magnitude]
    return catalog


def select_from_catalog(catalog, mag):
    """This function selects stars from catalog.
    Parameters
    -----------
    catalog: astropy table object
            Star catalog
    mag: float
        Function selects stars from catalog below given threshold
    Returns
    -------
    result: astropy table object
            selected catalosg stars
    """
    catalog = Table.to_pandas(catalog)
    catalog = catalog[(catalog['Vmag'] < mag)]
    reduced_catalog = catalog[(catalog['VarFlag'] != 3) & (catalog['VarFlag'] != 2)]
    reduced_catalog = reduced_catalog.dropna(subset=['RA_ICRS_'])
    result = Table.from_pandas(reduced_catalog)
    return result


def transform_catalog(ra_catalog, dec_catalog, time, cam):
    """This function transforms star coordinates (ra, dec) from a catalog to altaz.
    Parameters
    -----------
    ra_catalog: array
                right ascension of catalog stars
    dec_catalog: array
                declination of catalog stars
    time: astropy timestamp
            timestamp of the image
    cam: string
        name of the used all sky camera
    Returns
    -------
    pos_altaz: astropy SkyCoord object
                Star positions in altaz at the given time.
    """
    pos = SkyCoord(ra=ra_catalog, dec=dec_catalog, frame='icrs', unit='deg')
    pos_altaz = pos.transform_to(AltAz(obstime=time, location=cam.location))
    return pos_altaz


def match_catalogs(catalog, image_stars, cam, time, magnitude):
    """This function compares star positions.
    Parameters
    -----------
    catalog: array
            Stars from a catalog.
    c: array
        Detected stars in an all sky camera image.
    cam: string
        name of the used all sky camera
    Returns
    -------
    c: arrray
        Pixel positions of the matching stars.
    catalog: array
        Pixel positions of the matching stars.
    """
    idxc, idxcatalog, d2d, d3d = catalog.search_around_sky(image_stars, Angle('0.5d'))
    matches_catalog = catalog[idxcatalog]
    magnitude_matches = magnitude[idxcatalog]
    matches_image = image_stars[idxc]
    if not matches_image:
        image_matches = 0
        catalog_matches = 0
    else:

        catalog_row, catalog_col = horizontal2pixel(matches_catalog.alt, matches_catalog.az, cam)
        catalog_size = np.ones(len(catalog_row))
        catalog_matches = np.array([catalog_row[:, 0], catalog_col[:, 0], catalog_size])
        image_row, image_col = horizontal2pixel(matches_image.alt, matches_image.az, cam)
        image_size = np.ones(len(image_row))
        image_matches = np.array([image_row[0], image_col[0], image_size])
    return image_matches, catalog_matches, magnitude_matches
