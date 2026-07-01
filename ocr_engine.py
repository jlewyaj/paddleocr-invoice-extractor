from paddleocr import PaddleOCR
from models import OCRLine
from pathlib import Path


class OCREngine:
    """Wraps PaddleOCR to extract lines of text from an image."""

    def __init__(self):
        # use_angle_cls=True lets PaddleOCR detect and correct rotated text
        self.ocr = PaddleOCR(
            use_angle_cls=True,
            lang="en"
        )
    
    def read(self, image):
        """Run OCR on `image` and return a list of OCRLine objects.

        `image` can be either a file Path or a numpy array (PaddleOCR
        accepts a file path string or an array, so Paths are converted).
        """

        if isinstance(image, Path):
            image = str(image)

        result = self.ocr.ocr(
            image,
            cls=True  # apply the angle classifier during recognition
        )

        return self.extract_lines(result)
    
    def extract_lines(self, result):
        """Flatten PaddleOCR's raw nested output into a simple list of
        OCRLine objects.

        PaddleOCR's result format is a list of pages, each containing a
        list of boxes shaped like: [bbox, (text, confidence)].
        """
        lines = []

        for image in result:
            for box in image:

                lines.append(
                    OCRLine(
                        text=box[1][0],        # recognized text
                        confidence=box[1][1],  # confidence score
                        bbox=box[0]             # bounding box coordinates
                    )
                )

        return lines
