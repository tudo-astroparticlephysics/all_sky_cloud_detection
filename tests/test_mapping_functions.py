import astropy.units as u
from pytest import approx


def test_round_trip():
    from all_sky_cloud_detection.mapping_functions import (
        mapping_functions, inverse_mapping_functions
    )

    f = 5 * u.mm
    for theta in [0, 10, 30, 50, 60, 80] * u.deg:

        for name, mapping_function in mapping_functions.items():
            r = mapping_function(theta=theta, focal_length=f)
            theta_back = inverse_mapping_functions[name](r=r, focal_length=f)

            assert theta.value == approx(theta_back.to(u.deg).value)
