# coding: utf-8
from all_sky_cloud_detection.cameras import CTA
from all_sky_cloud_detection.catalog import read_catalog
c = read_catalog(max_magnitude=CTA.max_magnitude)
c
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
img = CTA.read('tests/resources/cta_images/starry.fits.gz')
img.data
img.time
img.timestamp
stars = SkyCoord(ra=c['ra'], dec=c['dec'])
altaz = AltAz(location=EarthLocation.of_site('Roque de los Muchachos'), obstime=img.timestamp)
stars_altaz = stars.transform_to(altaz)
