from scipy.io import loadmat
from astropy.io import fits
from astropy.time import Time
import astropy.units as u
from astropy.coordinates import EarthLocation
import dateutil.parser
import os
import json
from pkg_resources import resource_string
import numpy as np

from .camera import Camera, Lens, Sensor
from .image import Image

magic2018_mapping = json.loads(resource_string(
    'all_sky_cloud_detection', 'resources/magic_mapping_spline.json'
).decode('utf-8'))


class CTA(Camera):
    '''
    CTA AllSkyCamera as described in
    https://www.epj-conferences.org/articles/epjconf/pdf/2015/08/epjconf-atmo2014_03007.pdf
    and operated at the MAGIC and Paranal sites
    '''
    max_magnitude = 6
    threshold = 0.0025

    # Sigma 4.5mm, f2.8
    lens = Lens(focal_length=4.44 * u.mm, mapping='equisolid_angle')

    # CTA AllSkyCamera uses a KAI-04022 image sensor
    # see http://www.qsimaging.com/docs/KAI-04022_Datasheet.pdf
    sensor = Sensor(
        resolution_col=2048,
        resolution_row=2048,
        width=15.15 * u.mm,
        height=15.15 * u.mm,
    )

    @staticmethod
    def read(path):
        name, ext = os.path.splitext(path)
        if ext == '.mat':
            data = loadmat(path)
            img = data['pic1']
            timestamp = Time(dateutil.parser.parse(data['UTC1']))

        with fits.open(path) as f:
            img = f[0].data
            timestamp = Time(dateutil.parser.parse(f[0].header['TIMEUTC']))

        img[np.isnan(img)] = 0.0
        img[img < 0.0] = 0.0

        return Image(img / 2**16, timestamp)


class DiffractionLimited340(Camera):
    max_magnitude = 4
    threshold = 0.0015

    lens = Lens(focal_length=1.45 * u.mm, mapping='equidistant')
    sensor = Sensor(
        resolution_row=480,
        resolution_col=640,
        width=4.8 * u.mm,
        height=3.6 * u.mm,
    )

    @staticmethod
    def read(path):
        with fits.open(path) as f:
            img = f[0].data
            timestamp = Time(f[0].header['DATE-OBS'])
            return Image(img / 2**16, timestamp)


class MAGIC2018(Camera):
    max_magnitude = 5.5
    threshold = 0.0025

    lens = Lens(
        focal_length=1.55 * u.mm,
        mapping='spline',
        tck=magic2018_mapping['tck'],
        tck_inv=magic2018_mapping['tck_inv'],
    )
    # see https://www.sxccd.com/trius-sx9
    sensor = Sensor(
        resolution_row=1040,
        resolution_col=1392,
        width=6.5 * u.mm,
        height=4.8 * u.mm,
    )

    @staticmethod
    def read(path):
        with fits.open(path) as f:
            img = f[0].data
            h = f[0].header
            timestamp = Time(h['DATE-OBS'] + 'T' + h['TIME-OBS'])
            return Image(img / 2**16, timestamp)


cta_la_palma = CTA(
    location=EarthLocation(
        lat='28.761870°',
        lon='-17.890777°',
        height=2200 * u.m
    ),
    zenith_row=1699 / 2,
    zenith_col=1699 / 2 - 2,
    rotation=2.75 * u.deg,
)

magic_2018 = MAGIC2018(
    location=EarthLocation(
        lat='28.761870°',
        lon='-17.890777°',
        height=2200 * u.m
    ),
    zenith_row=MAGIC2018.sensor.resolution_row / 2 + 7,
    zenith_col=MAGIC2018.sensor.resolution_col / 2 + 33,
    rotation=171 * u.deg,
)


iceact = DiffractionLimited340(
    location=EarthLocation(
        lat=-89.99 * u.deg,
        lon=-63.45 * u.deg,
        height=2801 * u.m,
    ),
    zenith_row=250,
    zenith_col=326.5,
    rotation=87 * u.deg,
)
