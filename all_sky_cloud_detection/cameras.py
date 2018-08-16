from scipy.io import loadmat
from astropy.io import fits
from astropy.time import Time
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
    lens = Lens(focal_length=4.5, mapping_function='equisolid_angle')

    # CTA AllSkyCamera uses a KAI-04022 image sensor
    # see http://www.qsimaging.com/docs/KAI-04022_Datasheet.pdf
    sensor = Sensor(resolution_col=2048, resolution_row=2048, width=15.15, height=15.15)

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


class IceAct(Camera):
    lens = Lens(focal_length=5, mapping_function='equidistant')
    sensor = Sensor(640, 480, 1000, 1000)
