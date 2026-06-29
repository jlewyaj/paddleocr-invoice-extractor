from paddleocr import PaddleOCR

ocr = PaddleOCR(use_angle_cls=True, lang="en")
result = ocr.ocr("media/sample4.jpg", cls=True)

invoice = {}

FIELD_MAP = {
    "Doctor": "doctor",
    "Patient": "patient",
    "Hospital": "hospital",
    "Receipt No": "receipt_no",
    "Receipt": "receipt_no",
    "Date": "date",
    "Total": "total"
}


def extract_value(current_text, next_text, label):
    value = (
        current_text
        .replace(label, "")
        .replace(":", "")
        .strip()
    )

    if not value:
        value = next_text
    
    return value


for image in result:
    for i, box in enumerate(image):
        current_text = box[1][0]
        
        if i + 1 < len(image):
            next_text = image[i+1][1][0]
        else:
            next_text = ""
        
        for label, key in FIELD_MAP.items():
            if label in current_text: 
                invoice[key] = extract_value(current_text, next_text, label)
                break


print(invoice)