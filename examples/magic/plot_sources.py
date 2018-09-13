# coding: utf-8
from argparse import ArgumentParser
from astropy.coordinates import SkyCoord, AltAz, concatenate
import matplotlib.pyplot as plt

from all_sky_cloud_detection.cameras import magic_2018
from all_sky_cloud_detection.plotting import (
    add_direction_labels, add_zenith_lines, plot_img
)


parser = ArgumentParser()
parser.add_argument('inputfile')
parser.add_argument('-o', '--output')
args = parser.parse_args()


source_names = ['Mrk 501', 'Mrk 421', '1ES 1959+650']
sources = concatenate([SkyCoord.from_name(n) for n in source_names])

img = magic_2018.read(args.inputfile)

altaz = AltAz(location=magic_2018.location, obstime=img.timestamp)
sources_altaz = sources.transform_to(altaz)


fig, ax, plot = plot_img(img.data)

add_direction_labels(magic_2018, ax=ax, color='crimson', weight='bold', size=14)
add_zenith_lines(magic_2018, ax=ax)

for name, source in zip(source_names, sources_altaz):
    row, col = magic_2018.horizontal2pixel(source)
    ax.plot(col, row, color='Gold', marker='o')
    ax.annotate(
        name, (col, row), (0, 5),
        textcoords='offset points', ha='center', va='bottom',
        color='Gold', size=12, weight='bold',
    )

if args.output:
    fig.savefig(args.output, dpi=300)
else:
    plt.show()
