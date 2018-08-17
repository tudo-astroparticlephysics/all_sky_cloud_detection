from scipy.io import loadmat
from astropy.io import fits
from astropy.time import Time
import astropy.units as u
from astropy.coordinates import EarthLocation
import dateutil.parser
import os

from .camera import Camera, Lens, Sensor
from .image import Image


class CTA(Camera):
    '''
    CTA AllSkyCamera as described in
    https://www.epj-conferences.org/articles/epjconf/pdf/2015/08/epjconf-atmo2014_03007.pdf
    and operated at the MAGIC and Paranal sites
    '''
    max_magnitude = 6

    # Sigma 4.5mm, f2.8
    lens = Lens(focal_length=4.44 * u.mm, mapping_function='equisolid_angle')

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
            return Image(img / 2**16, timestamp)

        with fits.open(path) as f:
            img = f[0].data
            timestamp = Time(dateutil.parser.parse(f[0].header['TIMEUTC']))
            return Image(img / 2**16, timestamp)


class DiffractionLimited340(Camera):
    lens = Lens(focal_length=1.45 * u.mm, mapping_function='equidistant')
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
