import matplotlib.pyplot as plt
from argparse import ArgumentParser
import numpy as np
from skimage.exposure import adjust_gamma, rescale_intensity
import astropy.units as u

from all_sky_cloud_detection.cameras import cta_la_palma as cam
from all_sky_cloud_detection.plotting import (
    add_blobs, add_zenith_lines, add_direction_labels, plot_img
)
from all_sky_cloud_detection.calculate_cloudiness import (
    calculate_cloudiness_weighted, calculate_cloudiness_simple
)
from all_sky_cloud_detection.star_detection import find_stars, find_matching_stars
from all_sky_cloud_detection.catalog import read_catalog, transform_catalog


parser = ArgumentParser()
parser.add_argument('--min-altitude', default=20.0, type=float)
parser.add_argument('--threshold', default=cam.threshold, type=float)
parser.add_argument('--max-magnitude', default=cam.max_magnitude, type=float)


images = [
    'tests/resources/cta_images/starry_nomoon.fits.gz',
    'tests/resources/cta_images/starry.fits.gz',
    'tests/resources/cta_images/partly_cloudy.fits.gz',
    'tests/resources/cta_images/cloudy.fits.gz',
]


def main():
    args = parser.parse_args()

    catalog = read_catalog(
        max_magnitude=args.max_magnitude,
        max_variability=None,
    )

    for path in images:
        img = cam.read(path)

        # create catalog of possibly visible stars and planets
        stars_catalog, magnitude = transform_catalog(
            catalog, img.timestamp, cam, min_altitude=args.min_altitude
        )

        # img.smoothed = gaussian(img.data, sigma=1.5)

        # find blobs in the image
        r, c, s = find_stars(img.data, threshold=args.threshold)

        found_altaz = cam.pixel2horizontal(r, c, img.timestamp)
        # only use blobs with alt > min_altitude
        mask = found_altaz.alt.deg > args.min_altitude
        idx, found = find_matching_stars(
            stars_catalog, found_altaz[mask], max_sep=0.25 * u.deg
        )

        print('Simple:  ', calculate_cloudiness_simple(found))
        print('Weighted:', calculate_cloudiness_weighted(magnitude, found))

        img.data[np.isnan(img.data)] = np.nanmin(img.data)
        img.data = adjust_gamma(rescale_intensity(img.data, (0, 1)), gamma=0.7)

        # plot that stuff
        fig, ax, plot = plot_img(img)
        fig.colorbar(plot)

        add_blobs(
            r[mask], c[mask], s[mask],
            color='C0',
            ax=ax,
        )

        add_blobs(
            *cam.horizontal2pixel(stars_catalog[found]),
            np.full(len(stars_catalog), 1.5),
            color='C2',
            ax=ax,
        )
        add_blobs(
            *cam.horizontal2pixel(stars_catalog[~found]),
            np.full(len(stars_catalog), 1.5),
            color='C1',
            ax=ax,
        )
        plt.legend([
            plt.Circle((0, 0), 0, edgecolor='C2', fill=False),
            plt.Circle((0, 0), 0, edgecolor='C1', fill=False),
        ], [
            'Found Catalog Stars',
            'Catalog stars without match'
        ])

        add_zenith_lines(cam, ax=ax)
        add_direction_labels(cam, ax=ax, color='crimson', weight='bold', size=14)
        plt.show()


if __name__ == '__main__':
    main()
