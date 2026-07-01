from ocr_engine import OCREngine
from parser import InvoiceParser
from file_loader import FileLoader
from image_preprocessor import ImagePreprocessor
from excel_writer import ExcelWriter
from pdf_converter import PDFConverter
from text_normalizer import TextNormalizer
from signature_detector import SignatureDetector

# Wire up the pipeline components. Dependencies (like PDFConverter into
# FileLoader) are passed in manually here rather than via a framework.
converter = PDFConverter()
loader = FileLoader(converter)
preprocessor = ImagePreprocessor()
ocr = OCREngine()
parser = InvoiceParser()
writer = ExcelWriter()
normalizer = TextNormalizer()
detector = SignatureDetector()

invoices = []

# Full pipeline, run per page:
#   load -> preprocess image -> OCR -> normalize text -> parse fields
for page in loader.load_pages("input"):
    image = preprocessor.preprocess(page.image)
    lines = ocr.read(page.image)          # NOTE: reads page.image (raw), not the preprocessed `image` above
    lines = normalizer.normalize(lines)
    invoice = parser.parse(page, lines)
    invoice.signature = detector.detect(page.image, lines)
    invoices.append(invoice)

# Write all parsed invoices out to Invoice_Extract.xlsx
writer.write(invoices)
