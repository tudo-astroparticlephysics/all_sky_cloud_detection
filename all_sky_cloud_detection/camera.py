
from all_sky_cloud_detection import camera_classes as camclass


def camera(cam):
    if cam == 'cta':
        return camclass.cta
    if cam == 'iceact':
        return camclass.iceact
