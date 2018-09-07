# coding: utf-8
from all_sky_cloud_detection.cameras import magic_2018
from all_sky_cloud_detection.catalog import read_catalog
from all_sky_cloud_detection.plotting import add_direction_labels, add_zenith_lines
from astropy.coordinates import SkyCoord, AltAz
import astropy.units as u
import matplotlib.pyplot as plt
from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument('inputfile')
parser.add_argument('-o', '--output')
args = parser.parse_args()

c = read_catalog(
    max_magnitude=magic_2018.max_magnitude,
    max_variability=None,
)

img = magic_2018.read(args.inputfile)

big_dipper = [54061, 53910, 58001, 59774, 62956, 65378, 67301]
dipper_mask = [row['HIP'] in big_dipper for row in c]


stars = SkyCoord(ra=c['ra'], dec=c['dec'])
altaz = AltAz(obstime=img.timestamp, location=magic_2018.location)
stars_altaz = stars.transform_to(altaz)
mask = (stars_altaz.alt.deg > 15) & (c['v_mag'] <= 3.5)

fig = plt.figure(figsize=(12, 9))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_axis_off()
ax.imshow(img.data, cmap='gray', vmax=0.2)



ax.plot(magic_2018.zenith_col, magic_2018.zenith_row, 'o')

add_direction_labels(magic_2018, ax=ax, color='crimson', weight='bold', size=14)
add_zenith_lines(magic_2018, ax=ax)


for i, m in enumerate([mask, dipper_mask]):
    row, col = magic_2018.horizontal2pixel(stars_altaz[m])
    p, = ax.plot(
        col,
        row,
        'o',
        color=f'C{i}',
        ms=8,
        mfc='none'
    )

if args.output:
    fig.savefig(args.output, dpi=300)
else:
    plt.show()
