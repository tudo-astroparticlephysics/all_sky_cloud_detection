from matplotlib.patches import Circle
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt
from all_sky_cloud_detection.preparation import normalize_image
from all_sky_cloud_detection.star_detection import find_stars
import numpy as np
from all_sky_cloud_detection.io import read_file


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


def plot_image_without_blobs(path, cam, time, show_plot=False, save_plot=False):
    """The function plots images where no matches are found between image and catalog stars
    Parameters
    -----------
    path: string
        image path
    cam: camera object
        name of the camera
    time: astropy timestamp
        timestamp of the image
    show_plot: bool
        If show_plot is True the plotted image is shown
    save_plot: bool
        If save_plot is True the plotted image is saved as png file
    """
    if save_plot is True or show_plot is True:
        image, file_type = read_file(path)
        image = normalize_image(image, scale=2**16)
        row, col, size = find_stars(image, threshold=cam.image.threshold)

        fig, ax = plt.subplots(1, 1)
        ax.imshow(
            image,
            cmap='gray',
            vmin=np.nanpercentile(image, 1),
            vmax=np.nanpercentile(image, 99),
            )
        add_blobs(row, col, size)

        if save_plot is True:
            if file_type == '.fits' or file_type == '.gz':
                plt.savefig('tests/'+str(time)+'.png', dpi=300)
                if file_type == '.mat':
                    plt.savefig('tests/'+str(time)+'.png', dpi=300)
        if show_plot is True:
            plt.show()
        plt.close()


def plot_image(path, cam, image_matches, limited_row, limited_col, time, show_plot=False, save_plot=False):
    """The function plots images where matches are found between image and catalog stars
    Parameters
    -----------
    path: string
        image path
    cam: camera object
        name of the camera
    image_matches: Array
        Array of matches between image and catalog stars
    limited_row: Array
        y coordinates of catalog stars in the given zenith angle range
    limited_col: Array
        x coordinates of catalog stars in the given zenith angle range
    time: astropy timestamp
        timestamp of the image
    show_plot: bool
        If show_plot is True the plotted image is shown
    save_plot: bool
        If save_plot is True the plotted image is saved as png file
    """
    if save_plot is True or show_plot is True:
        image, file_type = read_file(path)
        image = normalize_image(image, scale=2**16)
        limited_size = np.ones(len(limited_col))
        fig, ax = plt.subplots(1, 1)
        ax.imshow(
            image,
            cmap='gray',
            vmin=np.nanpercentile(image, 1),
            vmax=np.nanpercentile(image, 99),
            )
        if len(str(image_matches)) == 1:
            add_blobs(limited_row, limited_col, limited_size*2)

        else:
            add_blobs(limited_row, limited_col, limited_size*2)
            add_blobs(image_matches[0], image_matches[1], image_matches[2]*2)
        if save_plot is True:
            if file_type == '.fits' or file_type == '.gz':
                plt.savefig('tests/'+str(time)+'.png', dpi=300)
            if file_type == '.mat':
                plt.savefig('tests/'+str(time)+'.png', dpi=300)
        if show_plot is True:
            plt.show()
        plt.close()
