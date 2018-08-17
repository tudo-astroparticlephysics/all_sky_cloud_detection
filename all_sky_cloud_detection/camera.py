from abc import ABCMeta, abstractmethod
from functools import partial
import astropy.units as u
from astropy.coordinates import SkyCoord, Angle
import numpy as np

from .mapping_functions import mapping_functions, inverse_mapping_functions


class Camera(metaclass=ABCMeta):
    '''
    Base class for All Sky Camera. Base classes need to set
    the lens, sensor, location and max_magnitude members and
    implement the read method, returning an instance of image

    Attributes
    ----------

    sensor: Sensor
        Sensor instance describing the sensor properties
    lens: Lens
        Lens instance describing the optical properties
    max_magnitude: float
        Maximum catalog magnitude to consider
    location: astropy.coordinates.EarthLocation
        Location of the all sky camera
    rotation: astropy.units.Quantity[angle] or astropy.coordinates.Angle
        maximum visiual magnitude of stars to take into account
    '''

    max_magnitude = 6

    @u.quantity_input(rotation=u.rad)
    def __init__(self, location, zenith_row, zenith_col, rotation=0 * u.deg,):
        self.location = location
        self.rotation = rotation
        self.zenith_row = zenith_row
        self.zenith_col = zenith_col

    @property
    @abstractmethod
    def lens(self):
        pass

    @abstractmethod
    def sensor(self):
        pass

    @classmethod
    @abstractmethod
    def read(path):
        '''
        Read an image file into an instance Image,
        must be overridden by subclasses
        '''
        pass

    @classmethod
    def theta2r(cls, theta):
        '''
        Calculates distance from the image center for a given incident angle

        Parameters
        -----------
        theta: float
                Polar angle between zenith and pixel position

        Returns
        -------
        float
            Distance between image center and pixel position
        '''

        return cls.lens.mapping_function(theta) / cls.sensor.pixel_width

    @classmethod
    def r2theta(cls, r):
        '''
        Calculates angle to the optical axes for a given distance to the image center

        Parameters
        -----------
        r: float
            distance between image center and point in mm

        Returns
        -------
        float
            Angle to the optical axis
        '''
        return cls.lens.inverse_mapping_function(r * cls.sensor.pixel_width)

    def pixel2horizontal(self, row, col):
        dr = row - self.zenith_row
        dc = col - self.zenith_col
        r = np.sqrt(dr**2 + dc**2)

        zenith = self.r2theta(r)

        az = np.arctan2(-dc, -dr) * u.rad + self.rotation

        return SkyCoord(
            alt=Angle('90d') - zenith,
            az=az,
            frame='altaz',
            location=self.location,
        )

    def horizontal2pixel(self, coord):
        r = self.theta2r(coord.zen)

        drow = -r * np.cos(coord.az - self.rotation)
        dcol = -r * np.sin(coord.az - self.rotation)

        row = drow + self.zenith_row
        col = dcol + self.zenith_col

        return row, col


class Lens:
    '''
    Class describing the lens of an AllSkyCamera.
    Needs to implem

    Attributes
    ----------
    mapping_function: string
        Descibes whether camera uses linear or non-linear mapping function.

    '''
    @u.quantity_input(focal_length=u.mm)
    def __init__(self, focal_length, mapping_function):
        self.focal_length = focal_length
        assert mapping_function in mapping_functions, 'Unsupported mapping_function'

        self.mapping_function = partial(
            mapping_functions[mapping_function],
            focal_length=self.focal_length,
        )
        self.inverse_mapping_function = partial(
            inverse_mapping_functions[mapping_function],
            focal_length=self.focal_length,
        )


class Sensor:
    '''
    Class containing image sensor properties

    Attributes
    ----------
    resolution_row: float
        Number of pixels in the image on the y axis
    resolution_col: float
        Number of pixels in the image on the x axis
    width: float
        Width of the sensor in mm
    height: float
        lenght of the sensor in mm
    '''
    @u.quantity_input(width=u.mm, height=u.mm)
    def __init__(self, resolution_row, resolution_col, width, height):
        self.resolution_row = resolution_row
        self.resolution_col = resolution_col
        self.width = width
        self.height = height
        self.pixel_width = self.width / self.resolution_col
