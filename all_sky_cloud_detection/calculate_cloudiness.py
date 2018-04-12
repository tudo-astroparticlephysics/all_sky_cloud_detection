
from all_sky_cloud_detection.coordinate_transformation import spherical2pixel
import numpy as np


def calculate_cloudiness(cam, catalog, matches):
    resolution_row = cam.sensor.resolution_row
    resolution_col = cam.sensor.resolution_col

    row, col = spherical2pixel(catalog.alt, catalog.az, cam.lens.theta2r, cam)

    row_reduced = row[((row) - (resolution_row/2))**2 + (col - (resolution_col/2))**2 < (245-25 / 2)**2]
    col_reduced = col[((row) - (resolution_row/2))**2 + (col - (resolution_col/2))**2 < (245-25 / 2)**2]
    size = np.ones(len(col_reduced))

    cl = np.round(1-matches/len(row_reduced), 2)
    return cl
