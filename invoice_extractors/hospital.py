from pathlib import Path

from rapidfuzz import fuzz, process

from .base import BaseExtractor


class HospitalExtractor(BaseExtractor):
    """Identifies the hospital/clinic name by fuzzy-matching OCR'd text
    against a known list of hospital names loaded from a reference file.
    """

    def __init__(self):
        hospital_file = Path("data/hospitals.txt")

        # Maps a normalized (uppercase, no-spaces) hospital name -> its
        # original, properly formatted name, for fast fuzzy lookups.
        self.hospitals = {}

        with hospital_file.open(encoding="utf-8") as f:
            for line in f:
                hospital = line.strip()

                if hospital:
                    self.hospitals[self.normalize(hospital)] = hospital

    def extract(self, lines):
        """Search the first few lines of the page for text that closely
        matches a known hospital name.
        """

        best_match = ""
        best_score = 0

        # Hospital is almost always near the top of the invoice, so we
        # only bother checking the first 8 lines.
        for line in lines[:8]:

            text = self.normalize(line.text)

            # Skip lines that are clearly not a hospital name (labels,
            # phone numbers, etc.) before doing the more expensive
            # fuzzy match.
            if not self.is_candidate(text):
                continue

            match = process.extractOne(
                text,
                self.hospitals.keys(),
                scorer=fuzz.token_set_ratio,
            )

            if not match:
                continue

            matched_key, score, _ = match

            # Keep track of the best-scoring match across all candidate lines
            if score > best_score:
                best_match = matched_key
                best_score = score

        # Only trust the match if it's reasonably confident
        if best_score >= 75:
            return self.hospitals[best_match]

        return ""

    def is_candidate(self, text):
        """Filter out lines that are unlikely to be a hospital name:
        known label words, mostly-numeric text, or text that's too short.
        """

        text = text.upper()

        blacklist = [
            "DR",
            "DOCTOR",
            "PRC",
            "DATE",
            "PATIENT",
            "OFFICIAL",
            "RECEIPT",
            "PHONE",
            "TEL",
            "FAX",
            "LICENSE",
            "AMOUNT",
            "TOTAL",
        ]

        if any(word in text for word in blacklist):
            return False

        digit_count = sum(c.isdigit() for c in text)

        # Skip lines that are mostly numbers (e.g. phone numbers, amounts)
        if digit_count > len(text) * 0.3:
            return False

        # Skip very short lines — unlikely to be a full hospital name
        if len(text) < 10:
            return False

        return True
    
    def normalize(self, text):
        """Uppercase and strip all spaces so text can be compared
        consistently regardless of OCR spacing inconsistencies.
        """
        return (
            text.upper()
            .replace(" ", "")
            .strip()
        )
