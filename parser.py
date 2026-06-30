import re
from models import Invoice


class InvoiceParser:

    FIELD_MAP = {
        "receipt_no": [
            "Receipt No",
            "Receipt #",
            "OR No",
            "OR #",
        ],
        "doctor": [
            "Attending Physician",
            "Physician",
            "Doctor",
            "Dr.",
        ],
        "prc_license": [
            "PRC License No",
            "PRC License",
            "PRC Lic. No",
            "PRC Lic",
            "License No",
            "License #",
        ],
        "patient": [
            "Name of Patient",
            "Patient Name",
            "Patient",
            "Client",
        ],
        "hospital": [
            "Medical Center",
            "Hospital",
            "Clinic",
        ],
        "date": [
            "Transaction Date",
            "Receipt Date",
            "Date",
        ],
        "total": [
            "Total Amount",
            "Grand Total",
            "Amount Due",
            "Total",
        ],
    }

    def __init__(self):
        self.cleaners = {
            "total": self.clean_amount,
            "receipt_no": self.clean_receipt_no,
        }

    def get_current_and_next_line(self, index, lines):
        current_line = lines[index]

        if index + 1 < len(lines):
            next_line = lines[index + 1]
        else:
            next_line = None

        return current_line, next_line

    def match_field(self, text):
        text = text.lower()

        for key, labels in self.FIELD_MAP.items():
            for label in labels:
                if label.lower() in text:
                    return key, label

        return None

    def clean_amount(self, value):
        return (
            value
            .replace("₱", "")
            .replace("P", "")
            .replace(",", "")
            .strip()
        )

    def clean_receipt_no(self, value):
        return (
            value
            .replace("No.", "")
            .replace("No", "")
            .strip()
        )

    def clean_text(self, value):
        return re.sub(r"\s+", " ", value).strip()

    def clean_value(self, key, value):
        cleaner = self.cleaners.get(key)

        if cleaner:
            value = cleaner(value)

        return self.clean_text(value)
    
    def is_label(self, text):
        text = text.lower()

        for labels in self.FIELD_MAP.values():
            for label in labels:
                if label.lower() in text:
                    return True

        return False
    
    def find_next_value(self, lines, start_index):
        for line in lines[start_index + 1:]:

            if not line.text.strip():
                continue

            if self.is_label(line.text):
                continue

            return line.text

        return ""

    def extract_value(self, current_line, lines, index, label):
        value = (
            current_line.text
            .replace(label, "")
            .replace(":", "")
            .strip()
        )

        if not value:
            value = self.find_next_value(lines, index)

        return value

    def parse(self, page, lines):
        invoice = Invoice(
            page=page.page_number,
            filename=page.filename,
        )
        

        for i in range(len(lines)):

            current_line = lines[i]

            field = self.match_field(current_line.text)g

            if not field:
                continue

            key, label = field

            value = self.extract_value(
                current_line,
                lines,
                i,
                label,
            )

            value = self.clean_value(
                key,
                value,
            )

            if not getattr(invoice, key):
                setattr(invoice, key, value)

        return invoice