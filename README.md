# all_sky_cloud_detection [![Build Status](https://travis-ci.org/tudo-astroparticlephysics/all_sky_cloud_detection.svg?branch=master)](https://travis-ci.org/tudo-astroparticlephysics/all_sky_cloud_detection)

A python package for the evaluation of the cloud coverage in all sky camera images.
The images are searched for stars as bright blobs and compared to a star catalog. 
Matching positions between detected stars in the image and catalog stars suggest a starry night sky, while catalog stars without matches in the image implay an overcast sky.

The package can be downloaded and installed with following commands:
```
$ git clone git@github.com:tudo-astroparticlephysics/all_sky_cloud_detection.git
$ cd all_sky_cloud_detection/
$ pip install .
```
Currently, `cameras.py` provides information of  all sky cameras located on La Palma and at the South Pole.
Code for the analysis of test images can be found [here](https://github.com/tudo-astroparticlephysics/all_sky_cloud_detection/tree/master/examples). 

