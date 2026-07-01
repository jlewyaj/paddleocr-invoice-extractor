import fitz  # PyMuPDF
import numpy as np
from models import Page


class PDFConverter:
    """Renders each page of a PDF into an image (numpy array) so it can
    be fed through the same preprocessing/OCR pipeline as regular images.
    """

    def pixmap_to_numpy(self, pix):
        """Convert a PyMuPDF Pixmap's raw byte buffer into a numpy array
        shaped (height, width, channels).
        """
        return np.frombuffer(
            pix.samples,
            dtype=np.uint8
        ).reshape(
            pix.height,
            pix.width,
            pix.n,  # number of color channels (e.g. 3 for RGB)
        )

    def convert(self, pdf_path):
        """Render every page of the PDF at pdf_path into a Page object
        containing a numpy image array. Returns a list of Page, one per
        page in the document, in order.
        """

        pages = []

        with fitz.open(pdf_path) as doc:

            for page in doc:

                # Render the page to a raster image at 200 DPI
                # (higher DPI = better OCR accuracy but slower/larger)
                pix = page.get_pixmap(
                    dpi=200
                )

                image = self.pixmap_to_numpy(pix)

                pages.append(
                    Page(
                        file=pdf_path,
                        page_number=page.number + 1,  # PyMuPDF pages are 0-indexed
                        image=image,
                    )
                )

        return pages
