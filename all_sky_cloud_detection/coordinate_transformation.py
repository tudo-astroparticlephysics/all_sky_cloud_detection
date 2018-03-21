from all_sky_cloud_detection.mapping_functions import r2theta, theta2r
import numpy as np
from astropy.coordinates import AltAz,EarthLocation,SkyCoord, Angle, CartesianRepresentation, CylindricalRepresentation
from astropy import units as u


angle = Angle('90d')


def spherical2pixel(theta, phi, mapping_function, cam):
	"""This function converts spherical coordinates to pixel coordinates.
	Parameters
	-----------
	theta:
			Polar angle in degrees
	phi:
		Azimuth angle in degrees
	mapping_function: string
						Mapping function, depending on the camera
	cam: string
		Name of the camera which took the images
	Returns
	-------
	row:
		Pixel coordinates on the y axis
	col:
		Pixel coordinates on the x axis
		"""
	radius = cam.image.radius
	zenith_row = cam.image.zenith_row
	zenith_col = cam.image.zenith_col
	az_off = cam.image.az_off
	pi = Angle('180d')
	z = np.array([np.zeros(len(theta))]).T
	r = mapping_function(radius, angle-theta)
	cylindrical = CylindricalRepresentation(r, phi+angle+az_off-2*pi, z)
	cartesian = cylindrical.represent_as(CartesianRepresentation)
	row = cartesian.x + zenith_row
	col = cartesian.y + zenith_col
	return row, col


def pixel2spherical(row, col, mapping_function, cam):
		"""This function converts pixel coordinates to spherical coordinates.
		Parameters
		-----------
		row:
			Pixel coordinates on the y axis
		col:
			Pixel coordinates on the x axis
		mapping_function: string
							Mapping function, depending on the camera
		cam: string
			Name of the camera which took the images
		Returns
		-------
		r:
			Distance between the pixel position and the image center
		theta:
				Polar angle in degrees
		phi:
			Azimuth angle in degrees
		"""
	radius = cam.image.radius
	zenith_row = cam.image.zenith_row
	zenith_col = cam.image.zenith_col
	az_off = cam.image.az_off
	row_start = np.ones(len(row))*zenith_row
	col_start = np.ones(len(row))*zenith_col
	z = np.zeros(len(row))
	row = row-row_start
	col = col-col_start
	cartesian = CartesianRepresentation(row, col, z)
	cylindrical = cartesian.represent_as(CylindricalRepresentation)
	r = cylindrical.rho
	phi = cylindrical.phi+Angle('90d')+(Angle('180d')-az_off)
	theta = Angle('90d')-Angle(mapping_function(radius, r))
	return  r, phi, theta
