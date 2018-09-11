from all_sky_cloud_detection.cameras import magic_2018
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import splev, splrep
import astropy.units as u
from scipy.optimize import minimize
from astropy.coordinates.angle_utilities import angular_separation
import json


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def f(params, row, col, alt, az):
    print(params)
    zenith_row, zenith_col, rotation = params

    magic_2018.zenith_row = zenith_row + magic_2018.sensor.resolution_row / 2
    magic_2018.zenith_col = zenith_col + magic_2018.sensor.resolution_col / 2
    magic_2018.rotation = rotation * u.deg
    magic_2018.lens.mapping = 'spline'

    r, phi = magic_2018.pixel2polar(row, col)
    r *= magic_2018.sensor.pixel_width.to(u.mm).value

    x = np.append(0, r)
    y = np.append(0, 90 - alt)

    idx = np.argsort(x)

    tck = splrep(
        x[idx], y[idx],
        t=np.linspace(np.percentile(x, 1), np.percentile(x, 99), 10)
    )
    magic_2018.lens.tck_inv = tck

    coords = magic_2018.pixel2horizontal(row, col)

    val =  angular_separation(alt * u.deg, az * u.deg, coords.alt, coords.az).value.mean()
    return val


df = pd.read_csv('magic_calib.csv')
df = df[df.alt > 13]

# plt.plot(magic_2018.pixel2polar(df.row, df.col)[0], 90 - df.alt)
# plt.show()


result = minimize(
    f,
    x0=[0, 0, 0],
    args=(df.row.values, df.col.values, df.alt.values, df.az.values)
)

assert result.success


r, phi = magic_2018.pixel2polar(df.row, df.col)
r *= magic_2018.sensor.pixel_width.to(u.mm).value

x = np.append(0, 90 - df.alt)
y = np.append(0, r)

idx = np.argsort(x)
idx_inv = np.argsort(y)

tck = splrep(
    x[idx], y[idx],
    t=np.linspace(np.percentile(x, 1), np.percentile(x, 99), 15)
)

tck_inv = splrep(
    y[idx_inv], x[idx_inv],
    t=np.linspace(np.percentile(y, 1), np.percentile(y, 99), 15)
)

plt.plot(x, y)
t = np.linspace(0, 78, 100)
plt.plot(t, splev(t, tck))
plt.show()


with open('magic_mapping_spline.json', 'w') as f:
    json.dump({'tck': tck, 'tck_inv': tck_inv}, f, cls=NumpyEncoder)
