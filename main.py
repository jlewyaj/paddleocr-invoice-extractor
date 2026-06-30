from ocr_engine import OCREngine
from parser import InvoiceParser
from file_loader import FileLoader
from excel_writer import ExcelWriter
from pdf_converter import PDFConverter

converter = PDFConverter()
loader = FileLoader(converter)
ocr = OCREngine()
parser = InvoiceParser()
writer = ExcelWriter()

invoices = []

for page in loader.load_pages("input"):
    result = ocr.read(str(page.image))
    invoice = parser.parse(result)
    invoice.page = page.page_number
    invoices.append(invoice)

writer.write(invoices)