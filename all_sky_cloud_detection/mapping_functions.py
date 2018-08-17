import numpy as np
import astropy.units as u


@u.quantity_input(theta=u.rad, focal_length=u.mm)
def gnomonical(theta, focal_length):
    return focal_length * np.tan(theta)


@u.quantity_input(theta=u.rad, focal_length=u.mm)
def stereographic(theta, focal_length):
    return 2 * focal_length * np.tan(theta / 2)


@u.quantity_input(theta=u.rad, focal_length=u.mm)
def equidistant(theta, focal_length):
    return focal_length * theta


@u.quantity_input(theta=u.rad, focal_length=u.mm)
def equisolid_angle(theta, focal_length):
    return 2 * focal_length * np.sin(theta / 2)


@u.quantity_input(theta=u.rad, focal_length=u.mm)
def orthographic(theta, focal_length):
    return focal_length * np.sin(theta)


@u.quantity_input(r=u.mm, focal_length=u.mm)
def inverse_gnomonical(r, focal_length):
    return np.arctan(r / focal_length)


@u.quantity_input(r=u.mm, focal_length=u.mm)
def inverse_stereographic(r, focal_length):
    return 2 * np.arctan(r / (2 * focal_length))


@u.quantity_input(r=u.mm, focal_length=u.mm)
def inverse_equidistant(r, focal_length):
    return r / focal_length


@u.quantity_input(r=u.mm, focal_length=u.mm)
def inverse_equisolid_angle(r, focal_length):
    return 2 * np.arcsin(r / (2 * focal_length))


@u.quantity_input(r=u.mm, focal_length=u.mm)
def inverse_orthographic(r, focal_length):
    return np.arcsin(r / focal_length)


mapping_functions = {
    'gnomonical': gnomonical,
    'stereographic': stereographic,
    'equidistant': equidistant,
    'equisolid_angle': equisolid_angle,
    'orthographic': orthographic,
}

inverse_mapping_functions = {
    'gnomonical': inverse_gnomonical,
    'stereographic': inverse_stereographic,
    'equidistant': inverse_equidistant,
    'equisolid_angle': inverse_equisolid_angle,
    'orthographic': inverse_orthographic,
}
