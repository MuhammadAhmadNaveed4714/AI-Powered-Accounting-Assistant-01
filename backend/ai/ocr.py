import easyocr
from ai.ocr_cleaner import clean_ocr_text

# Load EasyOCR Reader
reader = easyocr.Reader(["en"], gpu=False)


def extract_text_from_image(image_path):
    """
    Extract text from an image using EasyOCR.

    Returns:
        original_text (str): Raw OCR output
        cleaned_text (str): OCR text after cleaning
    """

    try:

        # OCR Extraction
        results = reader.readtext(
            image_path,
            detail=0
        )

        original_text = "\n".join(results)

        print("\n===== ORIGINAL OCR =====\n")
        print(original_text)

        # Clean OCR Output
        cleaned_text = clean_ocr_text(original_text)

        print("\n===== CLEANED OCR =====\n")
        print(cleaned_text)

        # Return BOTH versions
        return original_text, cleaned_text

    except Exception as e:

        print(f"\nOCR Error: {e}")

        return "", ""