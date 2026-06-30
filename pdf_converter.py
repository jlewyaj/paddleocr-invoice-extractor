import fitz
import numpy as np
from models import Page


class PDFConverter:

    def convert(self, pdf_path):
        doc = fitz.open(pdf_path)

        pages = []

        for page in doc:

            pix = page.get_pixmap(
                matrix=fitz.Matrix(10, 10)
            )

            image = np.frombuffer(
                pix.samples,
                dtype=np.uint8
            ).reshape(
                pix.height,
                pix.width,
                pix.n
            )

            pages.append(
                Page(
                    filename=pdf_path.name,
                    page_number=page.number + 1,
                    image=image,
                )
            )

        print(type(pages[0]))
        print(pages[0].shape)
        return pages