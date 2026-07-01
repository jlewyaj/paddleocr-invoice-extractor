from ocr_engine import OCREngine
from parser import InvoiceParser
from file_loader import FileLoader
from image_preprocessor import ImagePreprocessor
from excel_writer import ExcelWriter
from pdf_converter import PDFConverter
from text_normalizer import TextNormalizer

converter = PDFConverter()
loader = FileLoader(converter)
preprocessor = ImagePreprocessor()
ocr = OCREngine()
parser = InvoiceParser()
writer = ExcelWriter()
normalizer = TextNormalizer()

invoices = []

for page in loader.load_pages("input"):
    image = preprocessor.preprocess(page.image)
    lines = ocr.read(page.image)
    lines = normalizer.normalize(lines)
    invoice = parser.parse(page, lines)
    invoices.append(invoice)

writer.write(invoices)