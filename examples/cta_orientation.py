# coding: utf-8
from all_sky_cloud_detection.cameras import cta_la_palma
from all_sky_cloud_detection.catalog import read_catalog
from astropy.coordinates import SkyCoord, AltAz
import astropy.units as u
import matplotlib.pyplot as plt

c = read_catalog(
    max_magnitude=cta_la_palma.max_magnitude,
    max_variability=None,
)

img = cta_la_palma.read('tests/resources/cta_images/starry.fits.gz')

big_dipper = [54061, 53910, 58001, 59774, 62956, 65378, 67301]
dipper_mask = [row['HIP'] in big_dipper for row in c]


stars = SkyCoord(ra=c['ra'], dec=c['dec'])
altaz = AltAz(obstime=img.timestamp, location=cta_la_palma.location)
stars_altaz = stars.transform_to(altaz)
mask = (stars_altaz.alt.deg > 15) & (c['v_mag'] <= 5)

fig = plt.figure(figsize=(8, 8))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_axis_off()
ax.imshow(img.data, cmap='gray', vmax=0.2)


for m in (mask, dipper_mask):
    row, col = cta_la_palma.horizontal2pixel(stars_altaz[m])
    ax.plot(
        col,
        row,
        'o',
        ms=8,
        mfc='none'
    )


for az, label in zip((0, 90, 180, 270), 'NESW'):
    coord = SkyCoord(
        alt='15d',
        az=az * u.deg,
        frame='altaz',
        location=cta_la_palma.location,
    )
    row, col = cta_la_palma.horizontal2pixel(coord)
    ax.text(col, row, label, color='w', weight=500, size=14)

fig.show()
