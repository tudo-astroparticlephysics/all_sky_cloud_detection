# coding: utf-8
import matplotlib.pyplot as plt
import numpy as np

from all_sky_cloud_detection.io import read_fits
from all_sky_cloud_detection.preparation import normalize_image
from all_sky_cloud_detection.star_detection import find_stars
from all_sky_cloud_detection.plotting import add_blobs


def find_blobs(img_name, format, threshold):

    if format == 'fits':
        scale = 2**16
    else:
        scale = 2**10
    image = normalize_image(read_fits(img_name), scale=scale)
    row, col, size = find_stars(image, threshold=threshold)

    fig, ax = plt.subplots(1, 1)

    ax.imshow(
        image,
        cmap='gray',
        vmin=np.nanpercentile(image, 1),
        vmax=np.nanpercentile(image, 99),
        )
    add_blobs(row, col, size, ax=ax)
    fig.tight_layout()
    plt.savefig(img_name+'_blobs.pdf', dpi=600)
    return row, col, size
