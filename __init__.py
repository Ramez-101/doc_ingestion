"""
Professional NLP Document Processor
Enterprise-grade AI-powered document processing and analysis
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "Senior Development Team"
__description__ = "Professional NLP Document Processor - Enterprise-grade AI-powered document processing"

# Package imports for easy access
from .pipeline.enhanced_pipeline import NLPPipeline
from .core.file_handler import handle_file_upload
from .core.text_normalizer import normalize_text

__all__ = [
    'NLPPipeline',
    'handle_file_upload', 
    'normalize_text'
]
