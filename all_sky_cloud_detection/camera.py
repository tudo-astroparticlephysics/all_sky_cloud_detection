from abc import ABCMeta, abstractmethod
import astropy.units as u
from astropy.coordinates import SkyCoord, Angle
import numpy as np
from scipy.interpolate import splev
from skimage.transform import rotate

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
    rotate_image: bool
        If True, rotate the image instead of the coordinate system
    '''

    max_magnitude = 6

    @u.quantity_input(rotation=u.rad)
    def __init__(self, location, zenith_row, zenith_col, rotation=0 * u.deg, rotate_image=False):
        self.location = location
        self.rotation = rotation
        self.rotate_image = rotate_image
        self.zenith_row = zenith_row
        self.zenith_col = zenith_col

    def rotate(self, img):
        img = rotate(
            img,
            angle=self.rotation.to(u.deg).value,
            center=(self.zenith_col, self.zenith_row)
        )
        r, c = np.arange(img.shape[0]), np.arange(img.shape[1])
        r, c = np.meshgrid(r, c)
        m = self.pixel2horizontal(r.T, c.T).alt.deg < 0
        img[m] = np.nanmin(img[~m])
        return img

    @property
    @abstractmethod
    def threshold(self):
        pass

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

    def pixel2polar(self, row, col):
        dr = row - self.zenith_row
        dc = col - self.zenith_col
        r = np.sqrt(dr**2 + dc**2)
        phi = np.arctan2(-dc, -dr)
        return r, phi * u.rad

    def polar2pixel(self, r, phi):
        row = self.zenith_row - r * np.cos(phi)
        col = self.zenith_col - r * np.sin(phi)
        return row, col

    def pixel2horizontal(self, row, col, time=None):
        r, phi = self.pixel2polar(row, col)

        zenith = self.r2theta(r)
        az = phi
        if not self.rotate_image:
            az += self.rotation

        return SkyCoord(
            alt=Angle('90d') - zenith,
            az=az,
            frame='altaz',
            location=self.location,
            obstime=time,
        )

    def horizontal2pixel(self, coord):
        r = self.theta2r(coord.zen)
        phi = coord.az
        if not self.rotate_image:
            phi -= self.rotation

        return self.polar2pixel(r, phi)


class Lens:
    '''
    Class describing the lens of an AllSkyCamera.

    If a Lens does not have one of the 4 implemented
    mapping functions (e.g. because of distortions),
    override `mapping_function` and `inverse_mapping`

    Attributes
    ----------
    mapping: string
        The mapping function of the lens, one of
        * "gnomonical" for non-fisheye lenses
        * "equidistant"
        * "stereographic"
        * "equisolid_angle", e.g. for the Sigma 4.5mm f2.8

    '''
    @u.quantity_input(focal_length=u.mm)
    def __init__(self, focal_length, mapping, tck=None, tck_inv=None):
        self.focal_length = focal_length
        self.mapping = mapping
        if mapping == 'spline':
            if tck is None:
                raise ValueError('tck must be given if mapping is spline')
            if tck_inv is None:
                raise ValueError('tck_inv must be given if mapping is spline')
            self.tck = tck
            self.tck_inv = tck_inv
        else:
            assert mapping in mapping_functions or mapping, 'Unsupported mapping_function'

    def mapping_function(self, theta):
        if self.mapping == 'spline':
            return splev(theta.to(u.deg).value, self.tck, ext=0) * u.mm

        return mapping_functions[self.mapping](
            theta=theta,
            focal_length=self.focal_length,
        )

    def inverse_mapping_function(self, r):
        if self.mapping == 'spline':
            return splev(r.to(u.mm).value, self.tck_inv, ext=0) * u.deg

        return inverse_mapping_functions[self.mapping](
            r=r,
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
