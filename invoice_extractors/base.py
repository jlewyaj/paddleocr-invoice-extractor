from abc import ABC, abstractmethod


class BaseExtractor(ABC):
    """Common interface and shared helpers for all field extractors.

    Each subclass implements `extract()` to pull one specific invoice
    field (date, doctor, total, etc.) out of a list of OCRLine objects.
    """

    @abstractmethod
    def extract(self, lines):
        """Return the extracted value as a string, or "" if not found."""
        pass

    def clean(self, text):
        """Collapse repeated/irregular whitespace into single spaces."""
        return " ".join(text.split())
