import os
import numpy as np
import matplotlib.pyplot as plt
from argparse import ArgumentParser
from astropy.coordinates import concatenate, match_coordinates_sky
import astropy.units as u
import pandas as pd
from tqdm import tqdm

from all_sky_cloud_detection.cameras import magic_2018
from all_sky_cloud_detection.catalog import read_catalog, transform_catalog, get_planets
from all_sky_cloud_detection.star_detection import find_stars
from all_sky_cloud_detection.plotting import add_blobs, add_zenith_lines


parser = ArgumentParser()
parser.add_argument('inputdir')
args = parser.parse_args()

catalog = read_catalog(
    max_magnitude=2.5,
    max_variability=None,
)


write_header = True
for path in tqdm(sorted(os.listdir(args.inputdir))):

    img = magic_2018.read(os.path.join(args.inputdir, path))

    if img.data.mean() > 0.030:
        continue

    stars_altaz = transform_catalog(catalog, img.timestamp, magic_2018)
    objects = concatenate([stars_altaz, get_planets(img.timestamp, magic_2018)])
    objects = objects[objects.alt.deg > 5]

    r, c, s = find_stars(img.data, 0.04)
    found_altaz = magic_2018.pixel2horizontal(r, c, img.timestamp)
    mask = found_altaz.alt.deg > 5

    r, c, s = r[mask], c[mask], s[mask]
    found_altaz = found_altaz[mask]

    idx, d2d, d3d = match_coordinates_sky(objects, found_altaz)
    mask = d2d < 1.0 * u.deg
    idx = idx[mask]

    pd.DataFrame(dict(
        row=r[idx],
        col=c[idx],
        alt=objects[mask].alt.deg,
        az=objects[mask].az.deg,
    )).to_csv('magic_calib.csv', mode='a', index=False, header=write_header)
    write_header = False

    # fig = plt.figure(figsize=(8, 8))
    # ax = fig.add_axes([0, 0, 1, 1])
    # ax.set_axis_off()
    # ax.imshow(img.data, cmap='gray', vmax=0.2)

    # add_blobs(r, c, s, ax=ax, color='C0')

    # add_blobs(r[idx], c[idx], np.full(len(idx), 3.0), color='C2')

    # add_blobs(
    #     *magic_2018.horizontal2pixel(objects),
    #     np.full(len(objects), 2.0),
    #     ax=ax,
    #     color='C1',
    # )
    # add_zenith_lines(magic_2018, ax=ax)


    # plt.show()
