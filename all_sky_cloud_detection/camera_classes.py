from astropy.coordinates import EarthLocation
import astropy.units as u
import numpy as np


class Camera:
    """This class contains information about sensors, lenses and images from all
     sky cameras. Predefiend classes include the CTA and IceAct all sky cameras

    Parameters
     -----------
    sensor : sensor object
            Describes camera sensor
    lens : lens object
            Describes camera lens
    image : image object
            Describes image parameters
    name: string
        Name of the all sky camera
    location: astropy earth location object
        Location of the all sky camera

    Returns
    -------
    camera class object
    """

    def __init__(self, name, location, lens, sensor, image, mag):
        self.sensor = sensor
        self.lens = lens
        self.image = image
        self.name = name
        self.location = location
        self.mag = mag


class Lens:

    """This class contains information about lens characteristics.

    Parameters
     -----------
    mapping function : string
                        Descibes whether camera uses linear or non-linear mapping function.

    Returns
    -------
    Lens obejct
    """
    def __init__(self, mapping_function):
        self.mapping_function = mapping_function

    def theta2r(self, radius, theta):
        """This function calculates distance between image center and pixel
         position from known polar angle between zenith and pixel position.
        Parameters
        -----------
        radius: float
                Radius of the image in pixels
        theta: float
                Polar angle between zenith and pixel position
        Returns
        -------
        float
            Distance between image center and pixel position in pixel
        """
        if self.mapping_function == 'lin':
            return radius/(np.pi*u.rad/2)*theta.to(u.rad)
        else:
            return 2/np.sqrt(2)*radius*np.sin(theta.to(u.rad)/2)

    def r2theta(self, radius, r):
        """This function calculates polar angle between zenith and pixel
        position from known distance between image center and pixel position.
        Parameters
        -----------
        radius: float
                Radius of the image in pixels
        r: float
            Distance between image center and pixel position
        Returns
        -------
        float
        Polar angle between zenith and pixel position in radians
        """
        if self.mapping_function == 'lin':
            return r*(np.pi*u.rad)/(2*radius)
        else:
            return 2*np.arcsin((np.sqrt(2)/2)*r*(1/radius))


class Sensor:
    """This class contains information about sensor characteristics.
    Parameters
    -----------
    resolution_row: float
                    Number of pixels in the image on the y axis
    resolution_col: float
                    Number of pixels in the image on the x axis
    width: float
            Width of the sensor in mm
    height: float
            lenght of the sensor in mm
    Returns
    -------
    Sensor class object
    """
    def __init__(self, resolution_row, resolution_col, width, height):
        self.resolution_row = resolution_row
        self.resolution_col = resolution_col
        self.width = width
        self.height = height


class Image:
    """This class contains information about image characteristics.
    Parameters
    -----------
    radius: float
            Radius of the image in pixels
    zenith_row: float
                Position of the zenith in the image in pixels on the y axis
    zenith_col: float
                Position of the zenith in the image in pixels on the x axis
    az_off: float
            Angle which describes the offset between the declination = 0 deg
            axis if the all sky camera is not adjusted right
    Returns
    -------
    Image class object
    """
    def __init__(self, radius, zenith_row, zenith_col, az_off, threshold, timestamp):
        self.radius = radius
        self.zenith_row = zenith_row
        self.zenith_col = zenith_col
        self.az_off = az_off
        self.threshold = threshold
        self.timestamp = timestamp


cta = Camera(
     'CTA',
     EarthLocation(lat=28.7594*u.deg, lon=-17.8761*u.deg, height=2200*u.m),
     Lens('nonlin'),
     Sensor(850, 850, 1000, 1000),
     Image(849, 849, 849, 87.1*u.deg, 0.003, 'TIMEUTC'),
     5.7
)

iceact = Camera(
     'iceact',
     EarthLocation(lat=-89.99*u.deg, lon=-63.45*u.deg, height=2801*u.m),
     Lens('lin'),
     Sensor(640, 480, 1000, 1000),
     Image(304.5, 250, 326.5, 3*u.deg, 0.000001, 'DATE-OBS'),
     3.5
)
