from models import Invoice

from invoice_extractors.receipt_no import ReceiptNoExtractor
from invoice_extractors.hospital import HospitalExtractor
from invoice_extractors.doctor import DoctorExtractor
from invoice_extractors.prc_license import PRCLicenseExtractor
from invoice_extractors.patient import PatientExtractor
from invoice_extractors.date import DateExtractor
from invoice_extractors.total import TotalExtractor


class InvoiceParser:
    """Coordinates a set of field-specific extractors to turn a page's
    normalized OCR lines into a fully populated Invoice object.

    Each field (receipt number, hospital, doctor, etc.) has its own
    dedicated extractor class, so parsing logic for each field can be
    developed/tested independently.
    """

    def __init__(self):
        # One extractor per Invoice field
        self.receipt_no = ReceiptNoExtractor()
        self.hospital = HospitalExtractor()
        self.doctor = DoctorExtractor()
        self.prc_license = PRCLicenseExtractor()
        self.patient = PatientExtractor()
        self.date = DateExtractor()
        self.total = TotalExtractor()

    def parse(self, page, lines):
        """Build an Invoice for `page` by running each extractor over
        the page's OCR `lines`.
        """

        invoice = Invoice(
            page=page.page_number,
        )

        invoice.receipt_no = self.receipt_no.extract(lines)
        invoice.hospital = self.hospital.extract(lines)
        invoice.doctor = self.doctor.extract(lines)
        invoice.prc_license = self.prc_license.extract(lines)
        invoice.patient = self.patient.extract(lines)
        invoice.date = self.date.extract(lines)
        invoice.total = self.total.extract(lines)

        return invoice
