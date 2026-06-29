from models import Invoice


class InvoiceParser:

    FIELD_MAP = {
        "receipt_no": [
            "Receipt No",
            "Receipt #",
            "OR No",
            "OR #",
            "Official Receipt",
        ],

        "doctor": [
            "Doctor",
            "Dr.",
            "Physician",
            "Attending Physician",
        ],

        "patient": [
            "Patient",
            "Patient Name",
            "Name of Patient",
            "Client",
        ],

        "hospital": [
            "Hospital",
            "Medical Center",
            "Clinic",
        ],

        "date": [
            "Date",
            "Receipt Date",
            "Transaction Date",
        ],

        "total": [
            "Total",
            "Total Amount",
            "Grand Total",
            "Amount Due",
        ]
    }

    def extract_value(self, current_text, next_text, label):
        value = (
            current_text
            .replace(label, "")
            .replace(":", "")
            .replace("₱", "")
            .replace(",", "")
            .strip()
        )

        if not value:
            value = next_text
        
        return value

    def parse(self, result):
        invoice = Invoice()

        for image in result:
            for i, box in enumerate(image):

                current_text = box[1][0]

                if i + 1 < len(image):
                    next_text = image[i+1][1][0]
                else:
                    next_text = ""

                for key, labels in self.FIELD_MAP.items():
                    for label in labels:
                        if label in current_text: 
                            value = self.extract_value(
                                current_text,
                                next_text,
                                label
                            )
                            setattr(invoice, key, value)

                            break
        
        return invoice
