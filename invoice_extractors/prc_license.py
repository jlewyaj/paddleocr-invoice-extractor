import re

from .base import BaseExtractor


class PRCLicenseExtractor(BaseExtractor):

    def extract(self, lines):

        for line in lines:

            if "prc" not in line.text.lower():
                continue

            match = re.search(r"\d+", line.text)

            if match:
                return match.group()

        return ""