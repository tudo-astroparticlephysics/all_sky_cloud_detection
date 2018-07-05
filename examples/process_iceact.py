from all_sky_cloud_detection.process_image import process_image
import pandas as pd

from all_sky_cloud_detection.camera_classes import iceact


images = [
    '../tests/resources/iceact_images/cloudy.fits','../tests/resources/iceact_images/starry.fits'
]

results = []

for img in images:
    cl, time, mean_brightness = process_image(img, cam=iceact, file_format='fits')

    results.append({
        'cloudiness': cl,
        'timestamp': time.iso,
        'mean_brightness': mean_brightness,
        'image': img,
    })

df = pd.DataFrame(results)


df.to_csv('cloudiness.csv')
