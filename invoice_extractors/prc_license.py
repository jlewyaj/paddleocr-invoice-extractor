import re

from .base import BaseExtractor


class PRCLicenseExtractor(BaseExtractor):
    """Finds the doctor's PRC (Professional Regulation Commission)
    license number in the OCR'd lines.
    """

    def extract(self, lines):

        for line in lines:

            # Only consider lines that mention "PRC" at all
            if "prc" not in line.text.lower():
                continue

            # Grab the first run of digits on that line as the license number
            match = re.search(r"\d+", line.text)

            if match:
                return match.group()

        return ""
