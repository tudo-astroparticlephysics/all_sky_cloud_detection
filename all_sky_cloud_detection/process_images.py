from all_sky_cloud_detection.process_image import process_image
import pandas as pd
import glob


def process_images(path, cam):
    results = []
    for img in glob.glob(path):
        try:
            cl, time, mean_brightness, number, moon_alt, moon_az = process_image(img, cam)
        except ValueError:
            print(img)
            continue
        results.append({
            'cloudiness': cl,
            'timestamp': time.iso,
            'mean_brightness': mean_brightness,
            'image': img,
            'number': number,
            'moon_alt': moon_alt,
            'moon_az': moon_az
            })

    df = pd.DataFrame(results)
    df.to_csv('cloudiness.csv')
    return df
