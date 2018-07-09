from matplotlib.patches import Circle
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt

from all_sky_cloud_detection.io import read_fits
from all_sky_cloud_detection.preparation import normalize_image
from all_sky_cloud_detection.star_detection import find_stars
import numpy as np


def add_blobs(rows, columns, sizes, ax=None):
    """The function draws circles around given pixel coordinates
    Parameters
    -----------
    rows: array
        pixel positions, y axis
    columns: array
        pixel positions, x axis
    sizes:array

    Returns
    -------
    star_circles:
    """
    if ax is None:
        ax = plt.gca()

    star_circles = PatchCollection([
        Circle((col, row), radius=4 * sigma)
        for row, col, sigma in zip(rows, columns, sizes)
    ])
    star_circles.set_facecolor('none')
    star_circles.set_edgecolor(next(ax._get_lines.prop_cycler).get('color'))

    ax.add_collection(star_circles)

    return star_circles


def plot_image(path, cam, image_matches, limited_row, limited_col):
    image = normalize_image(read_fits(path), scale=2**16)
    row, col, size = find_stars(image, threshold=cam.image.threshold)
    limited_size = np.ones(len(limited_col))
    fig, ax = plt.subplots(1, 1)
    ax.imshow(
        image,
        cmap='gray',
        vmin=np.nanpercentile(image, 1),
        vmax=np.nanpercentile(image, 99),
        )
    add_blobs(limited_row, limited_col, limited_size)
    add_blobs(image_matches[0], image_matches[1], image_matches[2]*2)
    plt.savefig('testfigure.png', dpi=300)
    plt.show()
    plt.clf()
