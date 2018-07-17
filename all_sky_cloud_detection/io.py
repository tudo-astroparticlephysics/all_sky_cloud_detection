from astropy.io import fits
import os
import scipy.io as sio


def read_file(path):
    filename, file_type = os.path.splitext(path)
    if file_type == '.fits' or file_type == '.gz':
        with fits.open(path) as f:
            image = f[0].data
    if file_type == '.mat':
        image = sio.loadmat(path)['pic1']
    return image, file_type
