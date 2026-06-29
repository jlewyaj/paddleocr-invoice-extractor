from dataclasses import dataclass


@dataclass
class Invoice:
    receipt_no: str = ""
    hospital: str = ""
    doctor: str = ""
    patient: str = ""
    date: str = ""
    total: str = ""