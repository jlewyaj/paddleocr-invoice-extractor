import re

from .base import BaseExtractor


class ReceiptNoExtractor(BaseExtractor):

    def extract(self, lines):

        for line in lines:

            text = (
                line.text.upper()
                .replace(" ", "")
                .replace("-", "")
            )

            match = re.search(
                r"(?:NOOR|ORNO|OR-?|OR)\s*(\d+)",
                text,
                re.IGNORECASE,
            )

            if match:
                return match.group(1)

        return ""