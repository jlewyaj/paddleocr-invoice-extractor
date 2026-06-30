from ocr_engine import OCREngine
from parser import InvoiceParser
from file_loader import FileLoader
from excel_writer import ExcelWriter


loader = FileLoader()
ocr = OCREngine()
parser = InvoiceParser()
writer = ExcelWriter()

invoices = []

for file in loader.load("media"):
    print(type(str(file)))
    result = ocr.read(str(file))
    invoice = parser.parse(result)
    invoices.append(invoice)

writer.write(invoices)