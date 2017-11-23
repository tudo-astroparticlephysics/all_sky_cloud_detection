# coding: utf-8
import matplotlib.pyplot  as plt
import numpy as np

from all_sky_cloud_detection.io import read_fits
from all_sky_cloud_detection.preparation import normalize_image
from all_sky_cloud_detection.star_detection import find_stars
from all_sky_cloud_detection.plotting import add_blobs


image = read_fits('../tests/resources/CTA_AllSkyCam_2016-01-04_23-39-11.mat_1.fits.gz')
image = normalize_image(image, scale=2**16)
row, col, size = find_stars(image, threshold=0.005)

fig, ax = plt.subplots(1, 1)

ax.imshow(
    image,
    cmap='gray',
    vmin=np.nanpercentile(image, 1),
    vmax=np.nanpercentile(image, 99),
)
add_blobs(row, col, size, ax=ax)
fig.tight_layout()
plt.show()
