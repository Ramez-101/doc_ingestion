"""
Core module for NLP Document Processor
Contains file handling, text extraction, and OCR functionality
"""

from .file_handler import handle_file_upload
from .text_normalizer import normalize_text
from .ocr_pipeline import extract_text_from_image, extract_text_from_scanned_pdf

__all__ = [
    'handle_file_upload',
    'normalize_text', 
    'extract_text_from_image',
    'extract_text_from_scanned_pdf'
]
