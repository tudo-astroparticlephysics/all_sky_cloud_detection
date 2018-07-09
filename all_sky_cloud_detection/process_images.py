from all_sky_cloud_detection.process_image import process_image
import pandas as pd
import glob


def process_images(path, cam, file_format):
    results = []
    for images in glob.glob(path):
        for img in images:
            cl, time, mean_brightness = process_image(img, cam, file_format)

            results.append({
                'cloudiness': cl,
                'timestamp': time.iso,
                'mean_brightness': mean_brightness,
                'image': img,
                })

            df = pd.DataFrame(results)
    df.to_csv('cloudiness.csv')
