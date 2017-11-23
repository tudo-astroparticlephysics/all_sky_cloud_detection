from matplotlib.patches import Circle
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt


def add_blobs(rows, columns, sizes, ax=None):
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
