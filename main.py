from paddleocr import PaddleOCR
from parser import InvoiceParser

ocr = PaddleOCR(use_angle_cls=True, lang="en")
result = ocr.ocr("media/sample4.jpg", cls=True)

parser = InvoiceParser()
invoice = parser.parse(result)

print(invoice)