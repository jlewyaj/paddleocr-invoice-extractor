import re

from .base import BaseExtractor


class ReceiptNoExtractor(BaseExtractor):
    """Finds the official receipt (OR) number in the OCR'd lines.

    Handles common OCR misreads of the "OR" label (e.g. letters
    swapped/merged as "NOOR" or "ORNO") before extracting the digits
    that follow it.
    """

    def extract(self, lines):

        for line in lines:

            # Strip spaces and hyphens so misreads like "O R - 1234" or
            # "OR-1234" both normalize to a form the regex can match
            text = (
                line.text.upper()
                .replace(" ", "")
                .replace("-", "")
            )

            # Match known variants of the "OR" (Official Receipt) label,
            # then capture the digits that immediately follow it
            match = re.search(
                r"(?:NOOR|ORNO|OR-?|OR)\s*(\d+)",
                text,
                re.IGNORECASE,
            )

            if match:
                return "OR-" + match.group(1)

        return ""
