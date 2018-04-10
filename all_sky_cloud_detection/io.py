from astropy.io import fits
import scipy.io as sio


def read_fits(path):
    with fits.open(path) as f:
        image = f[0].data
    return image


def read_matlab(path):
    image = sio.loadmat(path)
    image = image['pic1']
    return image
