from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class Invoice:
    filename: str = ""
    page: int = 0
    receipt_no: str = ""
    hospital: str = ""
    doctor: str = ""
    prc_license: str = ""
    patient: str = ""
    date: str = ""
    total: str = ""


@dataclass
class Page:
    file: Path
    page_number: int
    image: Any

    @property
    def filename(self):
        return self.file.name

    @property
    def stem(self):
        return self.file.stem

    @property
    def extension(self):
        return self.file.suffix.lower()
    

@dataclass
class OCRLine:
    text: str
    confidence: float
    bbox: list
