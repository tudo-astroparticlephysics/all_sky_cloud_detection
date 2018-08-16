from scipy.io import loadmat
from astropy.io import fits
from astropy.time import Time
import dateutil.parser
import os

from .camera import Camera, Lens, Sensor
from .image import Image


class CTA(Camera):
    lens = Lens(focal_length=5, mapping_function='equisolid_angle')
    sensor = Sensor(resolution_col=1699, resolution_row=1699, width=1000, height=1000)

    def read(self, path):
        name, ext = os.path.splitext(path)
        if ext == '.mat':
            data = loadmat(path)
            img = data['pic1']
            timestamp = Time(dateutil.parser.parse(data['UTC1']))
            return Image(img / 2**16, timestamp, camera=self)

        with fits.open(path) as f:
            img = f[0].data
            timestamp = Time(dateutil.parser.parse(f[0].header['TIMEUTC']))
            return Image(img / 2**16, timestamp, camera=self)


class IceAct(Camera):
    lens = Lens(focal_length=5, mapping_function='equidistant')
    sensor = Sensor(640, 480, 1000, 1000)
