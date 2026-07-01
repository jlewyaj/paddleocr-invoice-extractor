import fitz
import numpy as np
from models import Page


class PDFConverter:

    def pixmap_to_numpy(self, pix):
        return np.frombuffer(
            pix.samples,
            dtype=np.uint8
        ).reshape(
            pix.height,
            pix.width,
            pix.n,
        )

    def convert(self, pdf_path):

        pages = []

        with fitz.open(pdf_path) as doc:

            for page in doc:

                pix = page.get_pixmap(
                    dpi=200
                )

                image = self.pixmap_to_numpy(pix)

                pages.append(
                    Page(
                        file=pdf_path,
                        page_number=page.number + 1,
                        image=image,
                    )
                )

        return pages