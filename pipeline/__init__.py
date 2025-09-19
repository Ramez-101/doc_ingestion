"""
Pipeline module for NLP Document Processor
Contains chunking, embedding, vector database, and pipeline functionality
"""

from .enhanced_pipeline import NLPPipeline
from .chunker import TextChunker
from .embedder import EmbeddingGenerator
from .vector_db import EnhancedVectorDB

# Backward compatibility imports
from .chunker import chunk_text
from .embedder import generate_embeddings
from .vector_db import VectorDB

__all__ = [
    'NLPPipeline',
    'TextChunker',
    'EmbeddingGenerator', 
    'EnhancedVectorDB',
    'chunk_text',
    'generate_embeddings',
    'VectorDB'
]
