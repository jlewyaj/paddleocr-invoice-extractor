class InvoiceParser:

    FIELD_MAP = {
        "Doctor": "doctor",
        "Patient": "patient",
        "Hospital": "hospital",
        "Receipt No": "receipt_no",
        "Receipt": "receipt_no",
        "Date": "date",
        "Total": "total"
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
        invoice = {}

        for image in result:
            for i, box in enumerate(image):

                current_text = box[1][0]

                if i + 1 < len(image):
                    next_text = image[i+1][1][0]
                else:
                    next_text = ""

                for label, key in self.FIELD_MAP.items():
                    if label in current_text: 
                        invoice[key] = self.extract_value(
                            current_text,
                            next_text,
                            label
                        )

                        break
        
        return invoice
