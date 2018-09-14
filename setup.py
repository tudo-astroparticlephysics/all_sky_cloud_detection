from setuptools import setup, find_packages


setup(
    name='all_sky_cloud_detection',
    author='Helena Nawrath,Maximilian Nöthe',
    author_email='helena.nawrath@tu-dortmund.de',
    version='0.2.0',
    packages=find_packages(),
    install_requires=[
        'scikit-image',
        'astropy>=3',
        'numpy',
        'scipy',
        'matplotlib',
    ],
    package_data={'all_sky_cloud_detection': ['resources/hipparcos.fits.gz']},
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
