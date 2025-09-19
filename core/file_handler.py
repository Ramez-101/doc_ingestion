import os
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

# Configuration constants
MAX_FILE_SIZE_MB = 100
SUPPORTED_EXTENSIONS = [".pdf", ".png", ".jpg", ".jpeg", ".txt"]

def validate_file(file_path: str) -> None:
    """Validate file before processing."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Check file size
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    if file_size_mb > MAX_FILE_SIZE_MB:
        raise ValueError(f"File too large: {file_size_mb:.1f}MB (max: {MAX_FILE_SIZE_MB}MB)")
    
    # Check file extension
    ext = Path(file_path).suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {ext}. Supported: {', '.join(SUPPORTED_EXTENSIONS)}")
    
    logger.info(f"File validation passed: {file_path} ({file_size_mb:.1f}MB)")

def handle_file_upload(file_path: str) -> str:
    """Returns extracted raw text based on file type with validation."""
    # Validate file first
    validate_file(file_path)
    
    ext = Path(file_path).suffix.lower()
    
    try:
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
            
    except Exception as e:
        logger.error(f"Failed to process file {file_path}: {e}")
        raise


def is_scanned_pdf(pdf_path: str) -> bool:
    """Heuristic: if no selectable text, likely scanned."""
    try:
        import pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages[:3]:  # check first 3 pages
                text = page.extract_text()
                if text and len(text.strip()) > 50:  # arbitrary threshold
                    return False
        return True
    except Exception as e:
        logger.error(f"Error checking if PDF is scanned: {e}")
        # Default to treating as scanned if we can't determine
        return True
