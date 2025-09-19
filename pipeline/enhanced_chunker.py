from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class TextChunker:
    """Enhanced text chunking with metadata and configuration options."""
    
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50, 
                 separators: List[str] = None):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators or ["\n\n", "\n", ". ", "! ", "? ", "; ", ": ", " ", ""]
        
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=self.separators,
            length_function=len,
            is_separator_regex=False
        )
    
    def chunk_text(self, text: str, doc_id: str = None) -> List[Dict[str, Any]]:
        """Split text into chunks with metadata.
        
        Returns:
            List of dictionaries containing:
            - text: chunk content
            - chunk_id: unique identifier
            - doc_id: document identifier
            - chunk_index: position in document
            - char_count: number of characters
            - word_count: approximate word count
        """
        if not text or not text.strip():
            logger.warning("Empty or whitespace-only text provided for chunking")
            return []
        
        raw_chunks = self.splitter.split_text(text)
        
        enhanced_chunks = []
        for i, chunk in enumerate(raw_chunks):
            chunk_data = {
                "text": chunk,
                "chunk_id": f"{doc_id}_{i}" if doc_id else f"chunk_{i}",
                "doc_id": doc_id,
                "chunk_index": i,
                "char_count": len(chunk),
                "word_count": len(chunk.split()),
                "chunk_size_config": self.chunk_size,
                "chunk_overlap_config": self.chunk_overlap
            }
            enhanced_chunks.append(chunk_data)
        
        logger.info(f"Created {len(enhanced_chunks)} chunks from text (length: {len(text)} chars)")
        return enhanced_chunks

# Backward compatibility function
def chunk_text(text: str, chunk_size: int = 500, chunk_overlap: int = 50) -> List[str]:
    """Legacy function for backward compatibility."""
    chunker = TextChunker(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks_with_metadata = chunker.chunk_text(text)
    return [chunk["text"] for chunk in chunks_with_metadata]
