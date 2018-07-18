import numpy as np
from all_sky_cloud_detection.coordinate_transformation import horizontal2pixel
from all_sky_cloud_detection.calculate_cloudiness import calculate_cloudiness
from all_sky_cloud_detection.time import get_time
from all_sky_cloud_detection.catalog import read_catalog, transform_catalog, match_catalogs
from all_sky_cloud_detection.star_selection import limit_zenith_angle, delete_big_blobs
from all_sky_cloud_detection.find_blobs import find_blobs
from all_sky_cloud_detection.camera_classes import iceact, cta
from all_sky_cloud_detection.io import read_file
from all_sky_cloud_detection.preparation import normalize_image
from all_sky_cloud_detection.plotting import plot_image, plot_image_without_blobs
from all_sky_cloud_detection.celestial_objects import moon_coordinates

def process_image(path, cam):
    """
    This function processes an image and returns a cloudiness parameter,
    the time the image was taken and the average pixel brightness.
    Parameters
    -----------
    path: str
        path to the image to be analyzed
    file_format: str
        file format of the images
    cam: camclass object
        camera

    Returns
    -------
    cloudiness: float
        Cloudiness of the analyzed images
    time: astropy.Time
        Timestamp of the images
    mean: float
        mean pixel brightness
    """

    catalog = read_catalog(max_magnitude=cam.mag)
    ra_catalog = catalog['ra']
    dec_catalog = catalog['dec']

    imagess, file_type = read_file(path)
    imagess = normalize_image(imagess, scale=2**16)
    imagess[np.isnan(imagess)] = np.nanmin(imagess)

    mean = np.mean(imagess)
    row, col, size = find_blobs(path, cam.image.threshold)
    row, col, size, number_big_blobs = delete_big_blobs(row, col, size)
    time = get_time(path, cam, file_type)
    moon_alt, moon_az = moon_coordinates(time, cam)
    image_catalog = limit_zenith_angle(row, col, cam, 30, time)
    number = len(image_catalog)
    if not (image_catalog):
        cloudiness = 1.0
    if len(image_catalog) > 1800 or len(image_catalog)==0 or number_big_blobs > 650:
        cloudiness = np.nan
    #    plot_image_without_blobs(path, cam, threshold)
        plot_image_without_blobs(path, cam, save_plot='no', show_plot='yes')

    else:
        image_row, image_col = horizontal2pixel(image_catalog.alt, image_catalog.az, cam)
        catalog = transform_catalog(ra_catalog, dec_catalog, time, cam)
        image_matches, catalog_matches, matches = match_catalogs(catalog, image_catalog, cam, time)
        #image_matches, catalog_matches = crop_moon(time, cam, image_matches, catalog_matches)
        #print(len(image_matches), len(catalog_matches))
        cloudiness, limited_row, limited_col = calculate_cloudiness(cam, catalog, matches, 30, time)
        plot_image(path, cam, image_matches, limited_row, limited_col, cloudiness, save_plot='yes', show_plot='no')

    return cloudiness, time, mean, number, moon_alt, moon_az
