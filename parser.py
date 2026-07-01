from models import Invoice

from invoice_extractors.receipt_no import ReceiptNoExtractor
from invoice_extractors.hospital import HospitalExtractor
from invoice_extractors.doctor import DoctorExtractor
from invoice_extractors.prc_license import PRCLicenseExtractor
from invoice_extractors.patient import PatientExtractor
from invoice_extractors.date import DateExtractor
from invoice_extractors.total import TotalExtractor


class InvoiceParser:

    def __init__(self):
        self.receipt_no = ReceiptNoExtractor()
        self.hospital = HospitalExtractor()
        self.doctor = DoctorExtractor()
        self.prc_license = PRCLicenseExtractor()
        self.patient = PatientExtractor()
        self.date = DateExtractor()
        self.total = TotalExtractor()

    def parse(self, page, lines):

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