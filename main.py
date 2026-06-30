from ocr_engine import OCREngine
from parser import InvoiceParser
from file_loader import FileLoader

loader = FileLoader()
ocr = OCREngine()
parser = InvoiceParser()

invoices = []

for file in loader.load("media"):
    print(type(str(file)))
    result = ocr.read(str(file))
    invoice = parser.parse(result)
    invoices.append(invoice)

print(invoices)