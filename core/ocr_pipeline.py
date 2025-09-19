import pytesseract
from pdf2image import convert_from_path
from PIL import Image

# Optional: Set Tesseract path if needed
# pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

def extract_text_from_image(image_path: str) -> str:
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, config='--psm 6')
    return text

def extract_text_from_scanned_pdf(pdf_path: str) -> str:
    images = convert_from_path(pdf_path, dpi=300)
    full_text = ""
    for img in images:
        text = pytesseract.image_to_string(img, config='--psm 6')
        full_text += text + "\n"
    return full_text