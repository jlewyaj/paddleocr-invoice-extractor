from .base import BaseExtractor


class DoctorExtractor(BaseExtractor):

    def extract(self, lines):

        for line in lines:

            text = self.clean(line.text)

            if text.lower().startswith("dr"):
                return text

        return ""