from openpyxl import Workbook
from pathlib import Path
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter


class ExcelWriter:

    def write(self, invoices, filename="Invoice_Extract.xlsx"):
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Invoices"

        # Header Row
        sheet.append([
            "Receipt No",
            "Hospital",
            "Doctor",
            "Patient",
            "Date",
            "Total",
        ])

        for cell in sheet[1]:
            cell.font = Font(bold=True)

        # Data Rows
        for invoice in invoices:
            if not any(vars(invoice).values()):
                continue
            
            sheet.append([
                invoice.receipt_no,
                invoice.hospital,
                invoice.doctor,
                invoice.patient,
                invoice.date,
                invoice.total,
            ])

        for column in sheet.columns:
            max_length = 0
            column_letter = get_column_letter(column[0].column)

            for cell in column:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))

            sheet.column_dimensions[column_letter].width = max_length + 2

        output = Path("output")
        output.mkdir(exist_ok=True)
        
        workbook.save(output/filename)