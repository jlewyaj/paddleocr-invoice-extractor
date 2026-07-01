import cv2
import numpy as np


class SignatureDetector:

    LABELS = [
        "SIGNATURE",
        "AUTHORIZED SIGNATURE",
        "AUTHORIZED PHYSICIAN",
        "ATTENDING PHYSICIAN",
        "PHYSICIAN",
    ]

    def detect(self, image, lines):

        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        page_h, page_w = gray.shape

        for line in lines:

            text = line.text.upper()

            if not any(label in text for label in self.LABELS):
                continue

            bbox = np.array(line.bbox, dtype=np.int32)

            xmin = bbox[:, 0].min()
            xmax = bbox[:, 0].max()
            ymin = bbox[:, 1].min()
            ymax = bbox[:, 1].max()

            margin_x = 150
            margin_top = 120
            margin_bottom = 120

            x1 = max(0, xmin - margin_x)
            x2 = min(page_w, xmax + margin_x)

            y1 = max(0, ymin - margin_top)
            y2 = min(page_h, ymax + margin_bottom)

            roi = gray[y1:y2, x1:x2]

            _, thresh = cv2.threshold(
                roi,
                180,
                255,
                cv2.THRESH_BINARY_INV,
            )

            # Remove the printed label itself
            label_y1 = max(0, ymin - y1 - 10)
            label_y2 = min(thresh.shape[0], ymax - y1 + 10)

            thresh[label_y1:label_y2, :] = 0

            contours, _ = cv2.findContours(
                thresh,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE,
            )

            for contour in contours:

                area = cv2.contourArea(contour)

                if area < 150:
                    continue

                x, y, w, h = cv2.boundingRect(contour)

                if w < 25:
                    continue

                if h < 8:
                    continue

                ratio = w / h

                if ratio > 12:
                    continue

                hull = cv2.convexHull(contour)

                solidity = area / cv2.contourArea(hull)

                if solidity > 0.95:
                    continue

                return "YES"

        return "NO"