import re
from unidecode import unidecode

def normalize_text(text: str) -> str:
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove non-printable chars
    text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
    # ASCII-fy (optional)
    text = unidecode(text)
    # Fix common OCR artifacts
    text = re.sub(r'(\w)-\s*\n\s*(\w)', r'\1\2', text)  # hyphenated line breaks
    text = re.sub(r'\n\s*\n', '\n\n', text)  # reduce multiple newlines
    return text.strip()