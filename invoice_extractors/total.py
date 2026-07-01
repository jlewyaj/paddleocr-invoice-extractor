import re

from .base import BaseExtractor


class TotalExtractor(BaseExtractor):

    MONEY_PATTERN = r"(?:PHP|₱|P)?\s*\d[\d,]*\.\d{2}"

    def extract(self, lines):

        amounts = []

        for line in lines:

            matches = re.findall(self.MONEY_PATTERN, line.text)

            amounts.extend(matches)

        if not amounts:
            return ""

        total = amounts[-1]

        return (
            total
            .replace("PHP", "")
            .replace("₱", "")
            .replace("P", "")
            .replace(",", "")
            .strip()
        )