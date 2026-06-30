from paddleocr import PaddleOCR
from models import OCRLine
from pathlib import Path


class OCREngine:

    def __init__(self):
        self.ocr = PaddleOCR(
            use_angle_cls=True,
            lang="en"
        )
    
    def read(self, image):

        if isinstance(image, Path):
            image = str(image)

        result = self.ocr.ocr(
            image,
            cls=True
        )

        return self.extract_lines(result)
    
    def extract_lines(self, result):
        lines = []

        for image in result:
            for box in image:

                lines.append(
                    OCRLine(
                        text=box[1][0],
                        confidence=box[1][1],
                        bbox=box[0]
                    )
                )

        return lines