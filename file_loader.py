from pathlib import Path
from models import Page


class FileLoader:

    SUPPORTED_EXTENSIONS  = [
        ".jpeg",
        ".jpg",
        ".png",
        ".pdf"
    ]

    def __init__(self, pdf_converter):
        self.pdf_converter = pdf_converter

    def load_pages(self, folder):

        folder = Path(folder)

        pages = []

        for file in sorted(folder.iterdir()):

            if file.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
                continue

            if file.suffix.lower() == ".pdf":
                pdf_pages = self.pdf_converter.convert(file)
                pages.extend(pdf_pages)
            else:
                pages.append(
                    Page(
                        file=file,
                        page_number=1,
                        image=file,
                    )
                )

        return pages