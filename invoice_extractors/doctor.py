from .base import BaseExtractor


class DoctorExtractor(BaseExtractor):
    """Finds the attending doctor's name in the OCR'd lines.

    Assumes the doctor's name appears on a line starting with "Dr"
    (e.g. "Dr. Juan Dela Cruz").
    """

    def extract(self, lines):

        for line in lines:

            text = self.clean(line.text)

            # Return the first line that starts with "Dr" (case-insensitive)
            if text.lower().startswith("dr"):
                return text

        return ""
