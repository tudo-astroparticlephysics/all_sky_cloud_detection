from astropy.io import fits


def read_fits(path):
    with fits.open(path) as f:
        image = f[0].data
    return image
