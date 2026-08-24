import easyocr
from ai.ocr_cleaner import clean_ocr_text

reader = None


def get_reader():
    global reader

    if reader is None:
        print("OCR: Initializing EasyOCR...", flush=True)

        reader = easyocr.Reader(
            ["en"],
            gpu=False,
            verbose=False
        )

        print("OCR: EasyOCR initialized.", flush=True)

    return reader


def extract_text_from_image(image_path):

    try:
        print("OCR: Starting image extraction...", flush=True)

        reader = get_reader()

        print("OCR: Running OCR...", flush=True)

        result = reader.readtext(image_path)

        print("OCR: OCR completed.", flush=True)

        original_text = " ".join(
            [item[1] for item in result]
        )

        cleaned_text = clean_ocr_text(original_text)

        print("OCR: Text cleaned successfully.", flush=True)

        return original_text, cleaned_text

    except Exception as e:

        print(f"OCR Error: {e}", flush=True)

        return "", ""
