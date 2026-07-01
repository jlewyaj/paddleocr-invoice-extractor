import re

from rapidfuzz import fuzz

from .base import BaseExtractor


class PatientExtractor(BaseExtractor):

    def extract(self, lines):

        for line in lines:

            text = self.clean(line.text)
            text = self.normalize(text)

            if not self.is_patient_line(text):
                continue

            name = self.extract_name(text)

            if name:
                return name

        return ""

    def is_patient_line(self, text):

        words = text.split()

        if not words:
            return False

        label = words[0].upper()

        if label == "PT":
            return True

        return fuzz.ratio(label, "PATIENT") >= 65

    def extract_name(self, text):

        parts = text.split(maxsplit=1)

        if len(parts) < 2:
            return ""

        name = parts[1]

        # BernardoQ -> Bernardo Q
        # AlejandroCruz -> Alejandro Cruz
        # ManaioLim -> Manaio Lim
        name = re.sub(
            r"([a-z])([A-Z])",
            r"\1 \2",
            name,
        )

        name = (
            name
            .replace(":", "")
            .replace("-", "")
            .strip()
        )

        if name.upper() in {"NAME", "NAME:", "PATIENT"}:
            return ""

        return name
    
    def normalize(self, text):
        text = re.sub(
            r"\bP\s*A\s*T\s*I\s*E\s*N\s*T\b",
            "Patient",
            text,
            flags=re.IGNORECASE,
        )

        return text