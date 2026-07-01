import re

from rapidfuzz import fuzz

from .base import BaseExtractor


class PatientExtractor(BaseExtractor):
    """Finds the patient's name in the OCR'd lines.

    Looks for a line that starts with a label like "Patient" or "PT",
    then extracts and cleans up the name that follows it.
    """

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
        """Check whether the line's first word looks like a "patient"
        label — either the exact abbreviation "PT" or something close
        enough to "PATIENT" via fuzzy string matching (to tolerate OCR
        misreads like "PSTIENT").
        """

        words = text.split()

        if not words:
            return False

        label = words[0].upper()

        if label == "PT":
            return True

        return fuzz.ratio(label, "PATIENT") >= 65

    def extract_name(self, text):
        """Pull the name portion out of a patient line (everything after
        the label) and clean up common OCR artifacts.
        """

        parts = text.split(maxsplit=1)

        if len(parts) < 2:
            return ""

        name = parts[1]

        # Insert a space where OCR merged two words together via a
        # lowercase-to-uppercase transition, e.g.:
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

        # Guard against accidentally "extracting" the label itself
        # (e.g. if the line was just "Patient Name:" with no actual name)
        if name.upper() in {"NAME", "NAME:", "PATIENT"}:
            return ""

        return name
    
    def normalize(self, text):
        """Collapse OCR text where "PATIENT" was split into individual
        letters (e.g. "P A T I E N T") back into a single word.
        """
        text = re.sub(
            r"\bP\s*A\s*T\s*I\s*E\s*N\s*T\b",
            "Patient",
            text,
            flags=re.IGNORECASE,
        )

        return text
