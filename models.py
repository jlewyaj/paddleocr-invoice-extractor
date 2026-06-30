from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class Invoice:
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
    filename: str
    page_number: int
    image: Any
