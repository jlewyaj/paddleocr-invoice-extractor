import re
from models import Invoice


class InvoiceParser:

    FIELD_MAP = {
        "receipt_no": [
            "Official Receipt",
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
        ]
    }

    def __init__(self):
        self.cleaners = {
            "total": self.clean_amount,
            "receipt_no": self.clean_receipt_no,
        }

    def get_current_and_next_text(self, i, image):
        current_text = image[i][1][0]
        if i + 1 < len(image):
            next_text = image[i+1][1][0]
        else:
            next_text = ""

        return current_text, next_text

    def match_field(self, current_text):
        for key, labels in self.FIELD_MAP.items():
            for label in labels:
                if label.lower() in current_text.lower():
                    return key, label
        return None

    def extract_value(self, current_text, next_text, label):
        value = (
            current_text
            .replace(label, "")
            .replace(":", "")
            .strip()
        )

        if not value:
            value = next_text
        
        return value

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
            value = self.clean_text(value)

        return value

    def parse(self, result):
        invoice = Invoice()

        for image in result:
            for i, _ in enumerate(image):
                
                current_text, next_text = self.get_current_and_next_text(i, image)

                field = self.match_field(current_text)
                
                if field:
                    key, label = field
                
                    value = self.extract_value(
                        current_text,
                        next_text,
                        label
                    )

                    value = self.clean_value(
                        key,
                        value
                    )

                    setattr(invoice, key, value)

        return invoice
