import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import logging

logger = logging.getLogger(__name__)

# Optional: Set Tesseract path if needed
# pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

def _check_tesseract_available():
    """Check if Tesseract OCR is available."""
    try:
        pytesseract.get_tesseract_version()
        return True
    except Exception as e:
        logger.error(f"Tesseract OCR not available: {e}")
        return False

def extract_text_from_image(image_path: str) -> str:
    """Extract text from image using OCR with error handling."""
    if not _check_tesseract_available():
        raise RuntimeError("Tesseract OCR is not installed or not accessible. Please install Tesseract OCR to process images.")
    
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image, config='--psm 6')
        logger.info(f"Successfully extracted text from image: {image_path}")
        return text
    except Exception as e:
        logger.error(f"Failed to extract text from image {image_path}: {e}")
        raise ValueError(f"Could not extract text from image: {e}")

def extract_text_from_scanned_pdf(pdf_path: str) -> str:
    """Extract text from scanned PDF using OCR with error handling."""
    if not _check_tesseract_available():
        raise RuntimeError("Tesseract OCR is not installed or not accessible. Please install Tesseract OCR to process scanned PDFs.")
    
    try:
        images = convert_from_path(pdf_path, dpi=300)
        full_text = ""
        for i, img in enumerate(images):
            logger.info(f"Processing page {i+1} of {len(images)} from PDF: {pdf_path}")
            text = pytesseract.image_to_string(img, config='--psm 6')
            full_text += text + "\n"
        logger.info(f"Successfully extracted text from scanned PDF: {pdf_path}")
        return full_text
    except Exception as e:
        logger.error(f"Failed to extract text from scanned PDF {pdf_path}: {e}")
        raise ValueError(f"Could not extract text from scanned PDF: {e}")
