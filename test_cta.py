# coding: utf-8
from all_sky_cloud_detection.cameras import CTA
from all_sky_cloud_detection.catalog import read_catalog
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
import astropy.units as u
import matplotlib.pyplot as plt
import numpy as np

c = read_catalog(max_magnitude=CTA.max_magnitude, max_variability=None)

location = EarthLocation.of_site('Roque de los Muchachos')
cam = CTA(location=location, rotation=2.75 * u.deg)
img = cam.read('tests/resources/cta_images/starry.fits.gz')

big_dipper = [54061, 53910, 58001, 59774, 62956, 65378, 67301]
dipper_mask = [row['HIP'] in big_dipper for row in c]


stars = SkyCoord(ra=c['ra'], dec=c['dec'])
altaz = AltAz(obstime=img.timestamp, location=location)
stars_altaz = stars.transform_to(altaz)

mask = (stars_altaz.alt.deg > 15) & (c['v_mag'] <= 5)

fig = plt.figure(figsize=(8, 8))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_axis_off()
ax.imshow(img.data, cmap='gray', vmax=0.2)

r = cam.theta2r(stars_altaz[mask].zen)
x = -r * np.sin(stars_altaz[mask].az - cam.rotation) + img.data.shape[1] / 2
y = -r * np.cos(stars_altaz[mask].az - cam.rotation) + img.data.shape[0] / 2

ax.plot(
    x, y,
    'o', ms=8, mfc='none',
)

r = cam.theta2r(stars_altaz[dipper_mask].zen)
x = -r * np.sin(stars_altaz[dipper_mask].az - cam.rotation) + img.data.shape[1] / 2
y = -r * np.cos(stars_altaz[dipper_mask].az - cam.rotation) + img.data.shape[0] / 2

ax.plot(
    x, y,
    'o', ms=8, mfc='none',
)

fig.show()
