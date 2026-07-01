import re

from .base import BaseExtractor


class DateExtractor(BaseExtractor):

    MONTHS = (
        "January|February|March|April|May|June|July|"
        "August|September|October|November|December|"
        "Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec"
    )

    DATE_PATTERNS = [
        r"\b\d{2}/\d{2}/\d{4}\b",
        r"\b\d{2}-\d{2}-\d{4}\b",
        rf"\b(?:{MONTHS})\s*\d{{1,2}}[.,]?\s*\d{{4}}\b",
    ]

    def extract(self, lines):

        dates = []

        for line in lines:
            text = self.normalize(line.text)

            for pattern in self.DATE_PATTERNS:
                match = re.search(pattern, text, re.IGNORECASE)

                if not match:
                    continue

                if "DATE" in text.upper():
                    return match.group()
                else:
                    dates.append(match.group())

        if dates:
            return dates[0]

        return ""

    def normalize(self, text):

        # Insert a space between month and day
        text = re.sub(
            rf"({self.MONTHS})(\d)",
            r"\1 \2",
            text,
            flags=re.IGNORECASE,
        )

        # Convert periods between day and year to commas
        # April30.2024 -> April 30, 2024
        text = re.sub(
            r"(\d{1,2})\.(\d{4})",
            r"\1, \2",
            text,
        )

        return text