from pathlib import Path
from models import Page


class FileLoader:
    """Scans an input folder and turns each supported file into one
    or more Page objects, ready for OCR processing.
    """

    # File types we know how to handle. Anything else is skipped.
    SUPPORTED_EXTENSIONS  = [
        ".jpeg",
        ".jpg",
        ".png",
        ".pdf"
    ]

    def __init__(self, pdf_converter):
        # Injected dependency: converts PDF files into Page objects (one per PDF page)
        self.pdf_converter = pdf_converter

    def load_pages(self, folder):
        """Walk `folder` in sorted order and build a flat list of Page objects.

        - PDFs are expanded into multiple pages via `pdf_converter`.
        - Image files become a single Page each (page_number=1).
        - Unsupported file types are silently ignored.
        """

        folder = Path(folder)

        pages = []

        for file in sorted(folder.iterdir()):

            # Skip anything that isn't an image or PDF
            if file.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
                continue

            if file.suffix.lower() == ".pdf":
                # A PDF can contain multiple pages, so extend (not append)
                pdf_pages = self.pdf_converter.convert(file)
                pages.extend(pdf_pages)
            else:
                # Plain image file: treat as a single-page document.
                # Note: `image` is set to the file path here; it gets
                # loaded/decoded later by the preprocessing/OCR step.
                pages.append(
                    Page(
                        file=file,
                        page_number=1,
                        image=file,
                    )
                )

        return pages
