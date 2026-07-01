import re

from .base import BaseExtractor


class TotalExtractor(BaseExtractor):
    """Finds the total amount charged on the invoice.

    Scans all lines for money-like values and assumes the *last* one
    found on the page is the total (since totals typically appear at
    the bottom of an invoice, after line items).
    """

    # Matches an optional currency prefix (PHP, ₱, or P) followed by a
    # number with optional thousands separators and exactly 2 decimal places
    # e.g. "PHP 1,234.56", "₱500.00", "P99.99", "1200.00"
    MONEY_PATTERN = r"(?:PHP|₱|P)?\s*\d[\d,]*\.\d{2}"

    def extract(self, lines):

        amounts = []

        for line in lines:

            matches = re.findall(self.MONEY_PATTERN, line.text)

            amounts.extend(matches)

        if not amounts:
            return ""

        # Assume the last money-like value found is the invoice total
        total = amounts[-1]

        # Strip currency markers and thousands separators, leaving a
        # plain numeric string
        return (
            total
            .replace("PHP", "")
            .replace("₱", "")
            .replace("P", "")
            .replace(",", "")
            .strip()
        )
