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
        self.timestamp = timestamp
