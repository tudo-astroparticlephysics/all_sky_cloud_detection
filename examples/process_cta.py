from all_sky_cloud_detection.process_images import process_images
from all_sky_cloud_detection.camera_classes import cta


df = process_images('/net/big-tank/POOL/projects/cta/all_sky_camera_images/la_palma/2015/2015_11_03-*', cta)

df.to_csv('/net/big-tank/POOL/users/hnawrath/results/la_palma_2015.csv')
