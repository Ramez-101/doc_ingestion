import os
from pathlib import Path


def handle_file_upload(file_path: str) -> str:
    """Returns extracted raw text based on file type."""
    ext = Path(file_path).suffix.lower()

    if ext == ".pdf":
        # Check if scanned or digital
        if is_scanned_pdf(file_path):
            from core.ocr_pipeline import extract_text_from_scanned_pdf
            return extract_text_from_scanned_pdf(file_path)
        else:
            from core.text_extractor import extract_text_from_digital_pdf
            return extract_text_from_digital_pdf(file_path)

    elif ext in [".png", ".jpg", ".jpeg"]:
        from core.ocr_pipeline import extract_text_from_image
        return extract_text_from_image(file_path)

    elif ext == ".txt":
        from core.text_extractor import extract_text_from_txt
        return extract_text_from_txt(file_path)

    else:
        raise ValueError(f"Unsupported file type: {ext}")


def is_scanned_pdf(pdf_path: str) -> bool:
    """Heuristic: if no selectable text, likely scanned."""
    import pdfplumber
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages[:3]:  # check first 3 pages
            text = page.extract_text()
            if text and len(text.strip()) > 50:  # arbitrary threshold
                return False
    return True