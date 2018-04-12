import glob
import numpy as np
from all_sky_cloud_detection.coordinate_transformation import spherical2pixel
from all_sky_cloud_detection.camera import camera
from all_sky_cloud_detection.calculate_cloudiness import calculate_cloudiness
from all_sky_cloud_detection.time import get_time
from all_sky_cloud_detection.catalog import read_catalog, transform_catalog, get_catalog, select_from_catalog, match_catalogs

from all_sky_cloud_detection.zenith_angle import zenith_angle
from all_sky_cloud_detection.find_blobs import find_blobs


def process_image(path, file_format, cam, threshold):
    cam = camera(cam)
    catalog = read_catalog('../tests/resources/hipparcos_catalog.csv')
    ra_catalog, dec_catalog = select_from_catalog(catalog, 4)
    cloudiness = []
    times = []
    for img_file in glob.glob(path):
        row, col, size = find_blobs(img_file, file_format, threshold)
        time = get_time(img_file)
        image_stars = zenith_angle(row, col, cam, 20, time)
        if not image_stars
            cloudiness.append(1)
            times.append(time)
        else:
            image_row, image_col = spherical2pixel(image_stars.alt, image_stars.az, cam.lens.theta2r, cam)
            image_size = np.ones(len(image_row[0]))
            catalog = transform_catalog(ra_catalog, dec_catalog, time, cam)

            image_matches, catalog_matches, matches = match_catalogs(catalog, image_stars, cam)
            cl = calculate_cloudiness(cam, catalog, matches)

            cloudiness.append(cl)
            times.append(time)
    return cloudiness, times
