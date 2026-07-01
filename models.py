from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class Invoice:
    """Holds the extracted fields for a single invoice/receipt.

    All fields default to empty/zero so a partially-parsed invoice
    (e.g. OCR failed on some fields) can still be created safely.
    """
    page: int = 0
    receipt_no: str = ""
    hospital: str = ""
    doctor: str = ""
    prc_license: str = ""
    patient: str = ""
    date: str = ""
    total: str = ""
    signature: str = ""


@dataclass
class Page:
    """Represents a single page of input (from an image file or a PDF page).

    `image` holds the actual pixel data (numpy array) once loaded/converted,
    or a Path if it hasn't been loaded yet (e.g. plain image files are
    passed through as their file path).
    """
    file: Path        # original source file this page came from
    page_number: int  # 1-indexed page number (always 1 for standalone images)
    image: Any         # numpy array of pixels, or a Path to the image file

    @property
    def filename(self):
        """Full filename including extension, e.g. 'invoice1.png'."""
        return self.file.name

    @property
    def stem(self):
        """Filename without extension, e.g. 'invoice1'."""
        return self.file.stem

    @property
    def extension(self):
        """Lowercased file extension, e.g. '.png'."""
        return self.file.suffix.lower()
    

@dataclass
class OCRLine:
    """A single line of text detected by the OCR engine."""
    text: str          # recognized text content
    confidence: float  # OCR engine's confidence score for this line
    bbox: list         # bounding box coordinates of the text on the page
