from abc import ABCMeta, abstractmethod
from functools import partial
import astropy.units as u

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
    location: astropy.coordinates.EarthLocation
        Location of the all sky camera
    location: float
        maximum visiual magnitude of stars to take into account
    '''

    max_magnitude = 6

    def __init__(self, location, rotation=0 * u.deg):
        self.location = location
        self.rotation = rotation

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


class Lens:
    '''
    Class describing the lens of an AllSkyCamera.
    Needs to implem

    Attributes
    ----------
    mapping_function: string
        Descibes whether camera uses linear or non-linear mapping function.

    '''
    def __init__(self, focal_length, mapping_function):
        self.focal_length = focal_length
        assert mapping_function in mapping_functions, 'Unsupported mapping_function'

        self.mapping_function = partial(
            mapping_functions[mapping_function],
            focal_length=self.focal_length,
        )
        self.inverse_mapping_functions = partial(
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
    def __init__(self, resolution_row, resolution_col, width, height):
        self.resolution_row = resolution_row
        self.resolution_col = resolution_col
        self.width = width
        self.height = height
        self.pixel_width = self.width / self.resolution_col
