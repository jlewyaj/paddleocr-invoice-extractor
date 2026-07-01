import cv2
import numpy as np


class ImagePreprocessor:

    def preprocess(self, image: np.ndarray) -> np.ndarray:

        image = self.to_grayscale(image)

        if self.is_dark(image):
            image = self.invert(image)

        image = self.enhance_contrast(image)
        image = self.denoise(image)

        return image

    def is_dark(self, image):
        return image.mean() < 120

    def to_grayscale(self, image):
        return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    def invert(self, image):
        return cv2.bitwise_not(image)

    def enhance_contrast(self, image):
        return cv2.equalizeHist(image)

    def denoise(self, image):
        return cv2.GaussianBlur(image, (3, 3), 0)