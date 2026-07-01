import re

from .base import BaseExtractor


class DateExtractor(BaseExtractor):
    """Finds the invoice date within the OCR'd lines.

    Looks for common date formats (MM/DD/YYYY, MM-DD-YYYY, or a month
    name followed by day and year). Prefers a match that appears on a
    line explicitly labeled "DATE"; otherwise falls back to the first
    date-like match found anywhere.
    """

    # Full and abbreviated month names, used to build date regexes
    MONTHS = (
        "January|February|March|April|May|June|July|"
        "August|September|October|November|December|"
        "Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec"
    )

    DATE_PATTERNS = [
        r"\b\d{2}/\d{2}/\d{4}\b",                       # e.g. 04/30/2024
        r"\b\d{2}-\d{2}-\d{4}\b",                        # e.g. 04-30-2024
        rf"\b(?:{MONTHS})\s*\d{{1,2}}[.,]?\s*\d{{4}}\b",  # e.g. April 30, 2024
    ]

    def extract(self, lines):
        """Scan all lines for date patterns.

        - If a matching line also contains the word "DATE", return that
          match immediately (high-confidence hit).
        - Otherwise, collect all date-like matches and, if the "DATE"
          label was never found, fall back to the first one collected.
        """

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
        """Fix common OCR spacing/punctuation issues that would
        otherwise break the date regex patterns.
        """

        # Insert a space between month and day
        # e.g. "April30" -> "April 30"
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
