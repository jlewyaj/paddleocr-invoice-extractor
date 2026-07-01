import cv2
import numpy as np


class ImagePreprocessor:
    """Cleans up a raw invoice image before it's sent to the OCR engine,
    to improve text recognition accuracy.
    """

    def preprocess(self, image: np.ndarray) -> np.ndarray:
        """Run the full preprocessing pipeline:
        grayscale -> (invert if dark) -> contrast enhancement -> denoise.
        """

        image = self.to_grayscale(image)

        # Scanned/photographed receipts sometimes come out with a dark
        # background (e.g. flash glare, negative-like scans). Inverting
        # these makes them look like normal dark-text-on-light-background.
        if self.is_dark(image):
            image = self.invert(image)

        image = self.enhance_contrast(image)
        image = self.denoise(image)

        return image

    def is_dark(self, image):
        """Heuristic: if the average pixel value is low, treat the image
        as having a dark background.
        """
        return image.mean() < 120

    def to_grayscale(self, image):
        """Convert a color image to single-channel grayscale."""
        return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    def invert(self, image):
        """Flip light/dark pixel values (negative effect)."""
        return cv2.bitwise_not(image)

    def enhance_contrast(self, image):
        """Histogram equalization to boost contrast, making text stand
        out more clearly from the background.
        """
        return cv2.equalizeHist(image)

    def denoise(self, image):
        """Light Gaussian blur to smooth out scan/compression noise
        without significantly blurring text edges.
        """
        return cv2.GaussianBlur(image, (3, 3), 0)
