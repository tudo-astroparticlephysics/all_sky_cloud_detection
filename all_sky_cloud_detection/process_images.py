from all_sky_cloud_detection.process_image import process_image
import pandas as pd
import glob


def process_images(path, cam):
    results = []
    for img in glob.glob(path):
        cl, time, mean_brightness, number = process_image(img, cam)
        results.append({
            'cloudiness': cl,
            'timestamp': time.iso,
            'mean_brightness': mean_brightness,
            'image': img,
            'number': number
            })

        df = pd.DataFrame(results)
    df.to_csv('cloudiness.csv')
    return df
