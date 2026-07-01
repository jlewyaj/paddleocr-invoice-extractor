from pathlib import Path

from rapidfuzz import fuzz, process

from .base import BaseExtractor


class HospitalExtractor(BaseExtractor):

    def __init__(self):
        hospital_file = Path("data/hospitals.txt")

        self.hospitals = {}

        with hospital_file.open(encoding="utf-8") as f:
            for line in f:
                hospital = line.strip()

                if hospital:
                    self.hospitals[self.normalize(hospital)] = hospital

    def extract(self, lines):

        best_match = ""
        best_score = 0

        # Hospital is almost always near the top
        for line in lines[:8]:

            text = self.normalize(line.text)

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

            if score > best_score:
                best_match = matched_key
                best_score = score

        if best_score >= 75:
            return self.hospitals[best_match]

        return ""

    def is_candidate(self, text):

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

        if digit_count > len(text) * 0.3:
            return False

        if len(text) < 10:
            return False

        return True
    
    def normalize(self, text):
        return (
            text.upper()
            .replace(" ", "")
            .strip()
        )