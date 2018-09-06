import numpy as np


class Image:
    '''
    Class to hold image data

    Attributes
    -----------
    img: np.ndarray
        numpy ndarray containing the image as grayscale float values,
        should be normalized to [0, 1.0]
    timestamp: astropy.time.Time
        Time when the image was taken
    timestamp: Camera
        Instance of the camera that took the picture
    '''
    def __init__(self, data, timestamp):
        self.data = data
        self.masked = data.copy()
        self.timestamp = timestamp

    def mask_inside_radius(self, radius, center_row, center_col):
        row = np.arange(self.data.shape[0])
        col = np.arange(self.data.shape[1])

        row, col = np.meshgrid(row, col)

        r = np.sqrt((row - center_row)**2 + (col - center_col)**2)

        self.masked[r <= radius] = 0.0

    def mask_outside_radius(self, radius, center_row, center_col):
        row = np.arange(self.data.shape[0])
        col = np.arange(self.data.shape[1])

        row, col = np.meshgrid(row, col)

        r = np.sqrt((row - center_row)**2 + (col - center_col)**2)

        self.masked[r >= radius] = 0.0

    def add_mask(self, img, threshold=0.5):
        self.masked[img <= threshold] = 0.0

    def reset_mask(self):
        self.masked = self.data.copy()
