from astropy.coordinates import SkyCoord, AltAz, get_body
import numpy as np
from astropy.table import Table
from pkg_resources import resource_filename
from functools import lru_cache


catalog_path = resource_filename('all_sky_cloud_detection', 'resources/hipparcos.fits.gz')


@lru_cache(maxsize=10)
def read_catalog(max_magnitude=None, max_variability=1):
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
    mask = np.isfinite(catalog['ra']) & np.isfinite(catalog['dec'])
    catalog = catalog[mask]
    if max_magnitude is not None:
        catalog = catalog[catalog['v_mag'] <= max_magnitude]

    if max_variability is not None:
        catalog = catalog[catalog['variability'] == 1]
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


def get_planets(time, cam):
    names = ['venus', 'mars', 'jupiter', 'saturn']
    altaz = AltAz(obstime=time, location=cam.location)
    planets = [
        get_body(b, time).transform_to(altaz)
        for b in names
    ]
    return SkyCoord(
        alt=[p.alt for p in planets],
        az=[p.az for p in planets],
        frame=altaz,
    )


def transform_catalog(catalog, time, cam, min_altitude=20):
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
    magnitude: array
        Magnitude of the stars
    """
    stars = SkyCoord(ra=catalog['ra'], dec=catalog['dec'], frame='icrs')
    stars_altaz = stars.transform_to(AltAz(obstime=time, location=cam.location))

    visible = stars_altaz.alt.deg > min_altitude
    stars_altaz = stars_altaz[visible]
    magnitude = catalog['v_mag'][visible]

    return stars_altaz, magnitude
