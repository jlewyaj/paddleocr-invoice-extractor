import re

from models import OCRLine


class TextNormalizer:
    """Cleans up raw OCR text output: fixes common misreads, spacing,
    currency symbols, and date formatting, so downstream parsers get
    more consistent input.
    """

    def normalize(self, lines):
        """Apply normalize_text() to every OCRLine, preserving
        confidence and bbox, and return the new list of OCRLine.
        """
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
        """Replace known OCR misreads (missing spaces, garbled words,
        misrecognized characters) with their correct forms.

        This is a lookup table built from patterns observed in real
        scanned invoices — extend it as new misreads are found.
        """

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
        """Fix dates OCR'd with a period instead of a comma before the
        year, e.g. 'June 5.2024' -> 'June 5, 2024'.
        """

        text = re.sub(
            r"([A-Za-z]+)\s+(\d{1,2})\.(\d{4})",
            r"\1 \2, \3",
            text,
        )

        return text

    def fix_spaces(self, text):
        """Collapse any run of whitespace (including newlines/tabs)
        into single spaces and trim the ends.
        """
        return " ".join(text.split())

    def normalize_currency(self, text):
        """Convert the literal text 'PHP' into the peso symbol."""

        text = text.replace("PHP", "₱")

        return text

    def normalize_text(self, text):
        """Run the full normalization pipeline on a single string, in order:
        1. collapse whitespace
        2. fix known OCR misreads
        3. normalize currency symbols
        4. fix date formatting
        """
        text = self.fix_spaces(text)
        text = self.fix_common_ocr_errors(text)
        text = self.normalize_currency(text)
        text = self.normalize_dates(text)

        return text
