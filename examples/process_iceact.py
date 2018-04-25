from all_sky_cloud_detection.process_image import process_image
import pandas as pd
import all_sky_cloud_detection.camera_classes as camclass
cl, time = process_image('../tests/resources/iceact/06/0613/0000.fits', 'fits', camclass.iceact)
df = pd.DataFrame({'cloudiness': cl, 'time': time})
cloudiness = df.to_csv('test.csv')
