from pathlib import Path


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

        for file in folder.iterdir():

            if file.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
                continue

            if file.suffix.lower() == "pdf":
                pages = self.pdf_converter.convert(str(file))
                pages.extend(pages)
            else:
                pages.append(str(file))

        return sorted(pages)