import pdfplumber
import logging

logger = logging.getLogger(__name__)

def extract_text_from_digital_pdf(pdf_path: str) -> str:
    """Extract text from digital PDF with error handling."""
    try:
        full_text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                # Handle multi-column: sort by x0 (left-to-right reading order)
                text = page.extract_text(x_tolerance=3, y_tolerance=3)
                if text:
                    full_text += text + "\n"
        return full_text
    except Exception as e:
        logger.error(f"Failed to extract text from PDF {pdf_path}: {e}")
        raise ValueError(f"Could not extract text from PDF: {e}")

def extract_text_from_txt(txt_path: str) -> str:
    """Extract text from TXT file with encoding fallback."""
    try:
        with open(txt_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        logger.warning(f"UTF-8 decoding failed for {txt_path}, trying fallback encodings")
        # Fallback to different encodings
        encodings = ['latin-1', 'cp1252', 'iso-8859-1']
        for encoding in encodings:
            try:
                with open(txt_path, 'r', encoding=encoding) as f:
                    logger.info(f"Successfully decoded {txt_path} using {encoding}")
                    return f.read()
            except UnicodeDecodeError:
                continue
        raise ValueError(f"Could not decode text file {txt_path} with any supported encoding")
    except Exception as e:
        logger.error(f"Failed to read text file {txt_path}: {e}")
        raise ValueError(f"Could not read text file: {e}")
