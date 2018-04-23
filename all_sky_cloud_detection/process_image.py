import glob
import numpy as np
from all_sky_cloud_detection.coordinate_transformation import horizontal2pixel
from all_sky_cloud_detection.calculate_cloudiness import calculate_cloudiness
from all_sky_cloud_detection.time import get_time
from all_sky_cloud_detection.catalog import read_catalog, transform_catalog, get_catalog, select_from_catalog, match_catalogs
from all_sky_cloud_detection.zenith_angle import zenith_angle
from all_sky_cloud_detection.find_blobs import find_blobs

def process_image(path, file_format, cam):
    """This function transforms star coordinates (ra, dec) from a catalog to altaz.
    Parameters
    -----------
    path: string
            path of the images to be analyzed
    file_format: string
                file format of the images
    cam: camera class object
        class of the all sky camera (camclass.cta or camclass.iceact)
    Returns
    -------
    cloudiness: list of floats
                Cloudiness of the analyzed images
    times: list of astropy timestamps
            Timestamp of the images
    """
    catalog = read_catalog('../tests/resources/hipparcos_catalog.csv')
    reduced_catalog = select_from_catalog(catalog, cam.mag)
    ra_catalog = reduced_catalog['RA_ICRS_']
    dec_catalog = reduced_catalog['DE_ICRS_']
    cloudiness = []
    times = []
    for img_file in glob.glob(path):
        row, col, size = find_blobs(img_file, file_format, cam.image.threshold)
        time = get_time(img_file, cam)
        image_catalog = zenith_angle(row, col, cam, 20, time)
        if not image_catalog:
            cloudiness.append(1)
            times.append(time)
        else:
            image_row, image_col = horizontal2pixel(image_catalog.alt, image_catalog.az, cam)
            image_size = np.ones(len(image_row[0]))
            catalog = transform_catalog(ra_catalog, dec_catalog, time, cam)
            c_matches, catalog_matches, matches = match_catalogs(catalog, image_catalog, cam, time)
            cl = calculate_cloudiness(cam, catalog, matches)
            cloudiness.append(cl)
            times.append(time)
    return cloudiness, times
