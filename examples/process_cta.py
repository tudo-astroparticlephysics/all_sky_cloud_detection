from all_sky_cloud_detection.process_image import process_image
import pandas as pd
from all_sky_cloud_detection.camera_classes import cta


images = [
    '../tests/resources/cta_images/cloudy.fits.gz', '../tests/resources/cta_images/starry.fits.gz', '../tests/resources/cta_images/partly_cloudy.fits.gz'
]

results = []

for img in images:
    cl, time, mean_brightness, moon_altitude = process_image(img, cam=cta)

    results.append({
        'cloudiness': cl,
        'timestamp': time.iso,
        'mean_brightness': mean_brightness,
        'image': img,
        'moon_altitude': moon_altitude
    })

df = pd.DataFrame(results)


df.to_csv('cloudiness_cta.csv')
