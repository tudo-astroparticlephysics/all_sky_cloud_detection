import numpy as np
from all_sky_cloud_detection.coordinate_transformation import horizontal2pixel
from all_sky_cloud_detection.calculate_cloudiness import calculate_cloudiness
from all_sky_cloud_detection.time import get_time
from all_sky_cloud_detection.catalog import transform_catalog, match_catalogs
from all_sky_cloud_detection.star_selection import limit_zenith_angle, delete_big_blobs
from all_sky_cloud_detection.find_blobs import find_blobs
from all_sky_cloud_detection.plotting import plot_image, plot_image_without_blobs
from all_sky_cloud_detection.celestial_objects import moon_coordinates
from all_sky_cloud_detection.star_selection import mean_pixel_brightness
from all_sky_cloud_detection.io import read_file
from all_sky_cloud_detection.catalog import read_catalog



def process_image(path, cam, show_plot=False, save_plot=False):
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
    show_plot: bool
        If show_plot is True the plotted image is shown
    save_plot: bool
        If save_plot is True the plotted image is saved as png file

    Returns
    -------
    cloudiness: float
        Cloudiness of the analyzed images
    time: astropy.Time
        Timestamp of the images
    mean: float
        mean pixel brightness
    moon_altitude: float
        sin(moon_altitude) of the moon in the image in rad
    """
    catalog = read_catalog(max_magnitude=cam.mag)
    magnitude = catalog['v_mag']
    image, file_type = read_file(path)
    mean_brightness = mean_pixel_brightness(image, file_type)
    image_row, image_col, image_size = find_blobs(path, cam.image.threshold)
    image_row, image_col, image_size, number_big_blobs = delete_big_blobs(image_row, image_col, image_size)
    time = get_time(path, cam, file_type)
    moon_altitude = moon_coordinates(time, cam)
    image_catalog = limit_zenith_angle(image_row, image_col, cam, cam.image.limit_zenith, time)
    if not (image_catalog):
        cloudiness = 1.0
    if len(image_catalog) > 1800 or len(image_catalog)== 0 or number_big_blobs > 650:
        cloudiness = np.nan
        plot_image_without_blobs(path, cam, time, save_plot=save_plot, show_plot=show_plot)

    else:
        ra_catalog = catalog['ra']
        dec_catalog = catalog['dec']
        image_row, image_col = horizontal2pixel(image_catalog.alt, image_catalog.az, cam)
        catalog = transform_catalog(ra_catalog, dec_catalog, time, cam)
        image_matches, catalog_matches, matches_magnitude = match_catalogs(catalog, image_catalog, cam, time, magnitude)
        cloudiness, limited_row, limited_col = calculate_cloudiness(cam, catalog, cam.image.limit_zenith, time, matches_magnitude, magnitude)
        plot_image(path, cam, image_matches, limited_row, limited_col, time, save_plot=save_plot, show_plot=show_plot)

    return cloudiness, time, mean_brightness, moon_altitude
