from matplotlib.patches import Circle
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord
import astropy.units as u
import numpy as np


def plot_img(img):

    fig = plt.figure(figsize=np.array(img.data.shape) / 100, dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()

    ax.imshow(
        img.data,
        cmap='gray',
        vmin=np.nanpercentile(img.data, 0.1),
        vmax=np.nanpercentile(img.data, 99),
    )

    return fig, ax


def add_blobs(rows, columns, sizes, color=None, ax=None):
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
        Circle((col, row), radius=3 * sigma)
        for row, col, sigma in zip(rows, columns, sizes)
    ])
    star_circles.set_facecolor('none')
    color = color or next(ax._get_lines.prop_cycler).get('color')

    star_circles.set_edgecolor(color)
    ax.add_collection(star_circles)

    return star_circles


def add_direction_labels(cam, ax=None, **kwargs):
    ax = ax or plt.gca()

    for az, label in zip((0, 90, 180, 270), 'NESW'):
        coord = SkyCoord(
            alt='15d',
            az=az * u.deg,
            frame='altaz',
        )
        row, col = cam.horizontal2pixel(coord)
        ax.text(col, row, label, **kwargs)


def add_zenith_lines(cam, step=10, ax=None, color='crimson', **kwargs):
    ax = ax or plt.gca()

    for zenith in np.arange(step, 91, step) * u.deg:
        c = Circle(
            xy=(cam.zenith_col, cam.zenith_row),
            radius=cam.theta2r(zenith),
            fill=False,
            edgecolor=color,
        )
        ax.add_artist(c)
