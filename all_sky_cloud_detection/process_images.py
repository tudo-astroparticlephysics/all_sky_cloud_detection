from all_sky_cloud_detection.process_image import process_image
import pandas as pd
import glob


def process_images(path, cam, show_plot=False, save_plot=False):
    results = []
    for img in glob.glob(path):
        try:
            cl, time, mean_brightness, moon_altitude = process_image(img, cam, show_plot, save_plot)
        except ValueError:
            print(img)
            continue
        results.append({
            'cloudiness': cl,
            'timestamp': time.iso,
            'mean_brightness': mean_brightness,
            'image': img,
            'moon_altitude': moon_altitude,
            })

    df = pd.DataFrame(results)
    df.to_csv('cloudiness.csv')
    return df
