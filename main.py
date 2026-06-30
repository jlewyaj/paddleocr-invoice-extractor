from ocr_engine import OCREngine
from parser import InvoiceParser

ocr = OCREngine()
parser = InvoiceParser()

result = ocr.read("media/sample4.jpg")
invoice = parser.parse(result)

print(invoice)