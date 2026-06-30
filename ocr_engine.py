from paddleocr import PaddleOCR


class OCREngine:

    def __init__(self):
        self.ocr = PaddleOCR(
            use_angle_cls=True,
            lang="en"
        )
    
    def read(self, image_path):
        result = self.ocr.ocr(
            image_path,
            cls=True
        )
        return result