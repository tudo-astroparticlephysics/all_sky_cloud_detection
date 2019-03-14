# all_sky_cloud_detection [![Build Status](https://travis-ci.org/tudo-astroparticlephysics/all_sky_cloud_detection.svg?branch=master)](https://travis-ci.org/tudo-astroparticlephysics/all_sky_cloud_detection)


Night Sky Cloud Coverage in All Sky Camera Images
---------------
A python package for the evaluation of the cloud coverage in all sky camera images.
The images are searched for stars as bright blobs and compared to a star catalog. 
Matching positions between detected stars in the image and catalog stars suggests a starry night sky, while catalog stars without matches in the image implay an overcast sky.

The package can be downloaded and installed with following commands:

```
$ git clone git@github.com:tudo-astroparticlephysics/all_sky_cloud_detection.git
$ cd all_sky_cloud_detection/
$ pip install .
```

##

Currently, `cameras` provides information of  all sky cameras located on La Palma and at the South Pole.
A test image from La Palma is given stored at

```python

images = '../tests/resources/cta_images/starry_nomoon.fits.gz'
```
All sky camera images are read in with a camera dependent function `cam.read`, supporting the image file format.

```python
import numpy as np
import astropy.units as u
from all_sky_cloud_detection.star_detection import find_stars, find_matching_stars

img = cam.read(images)
```
Stars in the images are detected, depending on their altitude, and converted into a horizontal coordinate system.

```python
r, c, s = find_stars(img.data, threshold=cam.threshold)
found_altaz = cam.pixel2horizontal(r, c, img.timestamp)

min_altitude = 20
mask = found_altaz.alt.deg > min_altitude
```
 A catalog of possibly visible stars is created with `read_catalog()` and `transform_catalog()`, which calculates the catalog star positions depending on the camera's loaction.

```python
from all_sky_cloud_detection.catalog import read_catalog, transform_catalog

catalog = read_catalog(
    max_magnitude=cam.max_magnitude,
    max_variability=None,
    )

stars_catalog, magnitude = transform_catalog(
    catalog, img.timestamp, cam, min_altitude=min_altitude
    )
  ```      
 `stars_catalog` is matched with the detected stars in the image and two cloudiness values are calculated.
 
 ```python
 
from all_sky_cloud_detection.calculate_cloudiness import (
calculate_cloudiness_weighted, calculate_cloudiness_simple
)
from skimage.exposure import adjust_gamma, rescale_intensity

idx, found = find_matching_stars(
    stars_catalog, found_altaz[mask], max_sep=0.25 * u.deg
    )

print('Simple:  ', calculate_cloudiness_simple(found))
print('Weighted:', calculate_cloudiness_weighted(magnitude, found))

```

Plot everything

```python
from all_sky_cloud_detection.plotting import (
    add_blobs, add_zenith_lines, add_direction_labels, plot_img
)
import matplotlib.pyplot as plt

img.data[np.isnan(img.data)] = np.nanmin(img.data)
img.data = adjust_gamma(rescale_intensity(img.data, (0, 1)), gamma=0.7)

fig, ax, plot = plot_img(img)
fig.colorbar(plot)
#add_blobs(
#    r[mask], c[mask], s[mask],
#    color='C0',
#    ax=ax,
#    )

add_blobs(
    *cam.horizontal2pixel(stars_catalog[found]),
    np.full(len(stars_catalog), 1.5),
    color='C2',
    ax=ax,
)
add_blobs(
    *cam.horizontal2pixel(stars_catalog[~found]),
    np.full(len(stars_catalog), 1.5),
    color='C1',
    ax=ax,
    )
plt.legend([
    plt.Circle((0, 0), 0, edgecolor='C2', fill=False),
    plt.Circle((0, 0), 0, edgecolor='C1', fill=False),
    ], [
    'Found Catalog Stars',
    'Catalog stars without match'
        ])

add_zenith_lines(cam, ax=ax)
add_direction_labels(cam, ax=ax, color='crimson', weight='bold', size=14)
plt.show()
```
