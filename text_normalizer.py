import re

from models import OCRLine


class TextNormalizer:

    def normalize(self, lines):
        normalized = []

        for line in lines:
            normalized.append(
                OCRLine(
                    text=self.normalize_text(line.text),
                    confidence=line.confidence,
                    bbox=line.bbox,
                )
            )

        return normalized
    
    def fix_common_ocr_errors(self, text):

        replacements = {
            "TOTALAMOUNT": "TOTAL AMOUNT",
            "TOTALAMOUNT.": "TOTAL AMOUNT",
            "AMOUNT(PHP)": "AMOUNT (PHP)",

            "PRC Lic Na": "PRC Lic No",
            "LICNa": "LIC No",

            "Pstie nt": "Patient",
            "Pstient": "Patient",

            "Dr. ": "Dr. ",
            "Dr.": "Dr. ",

            "ORNOR": "OR",
        }

        for old, new in replacements.items():
            text = text.replace(old, new)

        return text
    
    def normalize_dates(self, text):

        text = re.sub(
            r"([A-Za-z]+)\s+(\d{1,2})\.(\d{4})",
            r"\1 \2, \3",
            text,
        )

        return text

    def fix_spaces(self, text):
        return " ".join(text.split())

    def normalize_currency(self, text):

        text = text.replace("PHP", "₱")

        return text

    def normalize_text(self, text):
        text = self.fix_spaces(text)
        text = self.fix_common_ocr_errors(text)
        text = self.normalize_currency(text)
        text = self.normalize_dates(text)

        return text