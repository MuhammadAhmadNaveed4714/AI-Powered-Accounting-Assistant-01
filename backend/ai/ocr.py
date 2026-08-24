import easyocr
from ai.ocr_cleaner import clean_ocr_text

reader = None


def get_reader():
    global reader

    if reader is None:
        print("========== OCR: START INITIALIZATION ==========", flush=True)

        print("OCR: Creating EasyOCR Reader...", flush=True)

        reader = easyocr.Reader(
            ["en"],
            gpu=False
        )

        print("OCR: EasyOCR Reader CREATED SUCCESSFULLY", flush=True)

    return reader


def extract_text_from_image(image_path):

    try:
        print("OCR: Starting image extraction...", flush=True)

        reader = get_reader()

        print("OCR: Reader ready, starting readtext...", flush=True)

        result = reader.readtext(image_path)

        print("OCR: readtext completed...", flush=True)

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
        print(f"\nOCR Error: {e}", flush=True)
        return "", ""