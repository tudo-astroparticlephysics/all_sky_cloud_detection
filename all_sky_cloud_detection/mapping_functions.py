import numpy as np
from astropy import units as u


def theta2r(radius, theta, how='lin'):
    return 2/np.sqrt(2)*radius*np.sin(theta.to(u.rad)/2)


def r2theta(radius, r, how='lin'):
    return 2*np.arcsin((np.sqrt(2)/2)*r*(1/radius))


def lin_angle(radius, theta):
    return radius/((90*u.deg).to(u.rad))*theta.to(u.rad)


def eq_area(radius, theta):
    return 2/np.sqrt(2)*radius*np.sin(theta.to(u.rad)/2)


def lin_angle_inv(radius, r):
    return r*((90*u.deg).to(u.rad))*(1/radius)


def eq_area_inv(radius, r):
    return 2*np.arcsin((np.sqrt(2)/2)*r*(1/radius))
