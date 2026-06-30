from dataclasses import dataclass


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
