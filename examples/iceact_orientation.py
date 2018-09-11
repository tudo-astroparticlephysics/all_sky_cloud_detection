from all_sky_cloud_detection.cameras import iceact
from all_sky_cloud_detection.catalog import read_catalog
from astropy.coordinates import SkyCoord, AltAz
import astropy.units as u
import matplotlib.pyplot as plt

c = read_catalog(
    max_magnitude=iceact.max_magnitude,
    max_variability=None,
)

img = iceact.read('tests/resources/iceact_images/starry.fits')


stars = SkyCoord(ra=c['ra'], dec=c['dec'])
altaz = AltAz(obstime=img.timestamp, location=iceact.location)
stars_altaz = stars.transform_to(altaz)
mask = (stars_altaz.alt.deg > 15) & (c['v_mag'] <= 2.5)

fig = plt.figure(figsize=(8, 8))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_axis_off()
ax.imshow(img.data, cmap='gray', vmax=0.2)


row, col = iceact.horizontal2pixel(stars_altaz[mask])
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
        location=iceact.location,
    )
    row, col = iceact.horizontal2pixel(coord)
    ax.text(col, row, label, color='w', weight=500, size=14)

fig.show()
