import fitz
import numpy as np


class PDFConverter:

    def convert(self, pdf_path):
        doc = fitz.open(pdf_path)

        pages = []

        for page in doc:

            pix = page.get_pixmap(
                matrix=fitz.Matrix(2, 2)
            )

            image = np.frombuffer(
                pix.samples,
                dtype=np.uint8
            ).reshape(
                pix.height,
                pix.width,
                pix.n
            )

            pages.append(image)

        print(type(pages[0]))
        print(pages[0].shape)
        return pages