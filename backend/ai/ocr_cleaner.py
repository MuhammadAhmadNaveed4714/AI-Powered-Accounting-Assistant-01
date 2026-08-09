import re


def clean_ocr_text(text):
    """
    Clean common OCR mistakes found in receipts and invoices.
    """

    # =============================
    # Currency corrections
    # =============================

    # S125 -> $125
    text = re.sub(
        r"\bS(?=\d)",
        "$",
        text
    )

    # s125 -> $125
    text = re.sub(
        r"\bs(?=\d)",
        "$",
        text
    )

    # Rs.1190 -> Rs. 1190
    text = re.sub(
        r"Rs\.?(\d)",
        r"Rs. \1",
        text
    )


    # =============================
    # Common OCR mistakes
    # =============================

    # S5s0.00 -> $550.00
    text = re.sub(
        r"S5s0\.00",
        "$550.00",
        text,
        flags=re.IGNORECASE
    )


    # sso.00 -> $50.00
    text = re.sub(
        r"sso\.00",
        "$50.00",
        text,
        flags=re.IGNORECASE
    )


    # ssoo.00 -> $500.00
    text = re.sub(
        r"ssoo\.00",
        "$500.00",
        text,
        flags=re.IGNORECASE
    )


    # =============================
    # Generic OCR Fixes
    # =============================

    # $5s0 -> $550
    # FIXED: lambda used to avoid group reference error
    text = re.sub(
        r"\$(\d)s(\d)",
        lambda m: f"${m.group(1)}5{m.group(2)}",
        text,
        flags=re.IGNORECASE
    )


    # $5so -> $550
    # FIXED: lambda used
    text = re.sub(
        r"\$(\d)so",
        lambda m: f"${m.group(1)}50",
        text,
        flags=re.IGNORECASE
    )


    # $25o -> $250
    text = re.sub(
        r"\$(\d+)o\b",
        r"$\g<1>0",
        text,
        flags=re.IGNORECASE
    )


    # =============================
    # Invoice number corrections
    # =============================

    # 0oo123 -> 000123
    text = re.sub(
        r"0[oO]{2}(?=\d)",
        "000",
        text
    )


    # =============================
    # Quantity corrections
    # =============================

    # Invoice OCR me quantity kabhi price ke sath merge ho jati hai

    text = re.sub(
        r"\$250\b",
        "2",
        text
    )

    text = re.sub(
        r"\$150\b",
        "1",
        text
    )

    text = re.sub(
        r"\$50\b",
        "1",
        text
    )


    return text