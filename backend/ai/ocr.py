import easyocr
from ai.ocr_cleaner import clean_ocr_text

reader = None


def get_reader():
    global reader

    if reader is None:
        print("Initializing EasyOCR...")
        reader = easyocr.Reader(["en"], gpu=False)

    return reader


def extract_text_from_image(image_path):

    try:
        reader = get_reader()

        result = reader.readtext(image_path)

        original_text = " ".join(
            [item[1] for item in result]
        )

        print("\n===== ORIGINAL OCR =====\n")
        print(original_text)

        cleaned_text = clean_ocr_text(original_text)

        print("\n===== CLEANED OCR =====\n")
        print(cleaned_text)

        return original_text, cleaned_text

    except Exception as e:
        print(f"\nOCR Error: {e}")
        return "", ""
