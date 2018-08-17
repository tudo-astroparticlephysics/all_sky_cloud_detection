from all_sky_cloud_detection.process_image import process_image
import pandas as pd
import glob


def process_images(path, cam, show_plot=False, save_plot=False, file_name='cloudiness'):
    """
    Process images from an allsky camera to get a cloudiness value.
    Results are saved in a csv file.

    Parameters
    -----------
    path: 'str'
        Path to the images to be analyzed
    cam: 'str'
        Camera
    show_plot: 'bool'
        If show_plot is True the plotted image is shown
    save_plot: class 'bool'
        If save_plot is True the plotted image is saved as png file
    file_name: 'str'

    Returns
    -------
    df: 'pandas.core.frame.DataFrame'
        Name of the file in which the results are saved.
    """
    results = []
    for img in glob.glob(path):
        try:
            cloudiness, time, mean_brightness, moon_altitude, sun_altitude = process_image(img, cam, show_plot, save_plot)
            print('hi')
        except ValueError:
            continue
        results.append({
            'cloudiness': cloudiness,
            'timestamp': time.iso,
            'mean_brightness': mean_brightness,
            'image': img,
            'moon_altitude': moon_altitude,
            'sun_altitude': sun_altitude,
            })

    df = pd.DataFrame(results)
    df.to_csv(str(file_name)+'.csv')

    return df
