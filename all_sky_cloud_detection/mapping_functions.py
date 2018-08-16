import numpy as np


def gnomonical(theta, focal_length):
    return focal_length * np.tan(theta)


def stereographic(theta, focal_length):
    return 2 * focal_length * np.tan(theta / 2)


def equidistant(theta, focal_length):
    return focal_length * theta


def equisolid_angle(theta, focal_length):
    return 2 * focal_length * np.sin(theta / 2)


def orthographic(theta, focal_length):
    return focal_length * np.sin(theta)


def inverse_gnomonical(r, focal_length):
    return np.arctan(r / focal_length)


def inverse_stereographic(r, focal_length):
    return 2 * np.arctan(r / (2 * focal_length))


def inverse_equidistant(r, focal_length):
    return r / focal_length


def inverse_equisolid_angle(r, focal_length):
    return 2 * np.arcsin(r / (2 * focal_length))


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
