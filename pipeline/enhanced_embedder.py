from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any, Optional
import logging
import numpy as np

logger = logging.getLogger(__name__)

class EmbeddingGenerator:
    """Enhanced embedding generation with model selection and error handling."""
    
    # Available models with their characteristics
    AVAILABLE_MODELS = {
        'all-MiniLM-L6-v2': {
            'dimensions': 384,
            'description': 'Fast and efficient, good for general use',
            'size': 'small'
        },
        'all-mpnet-base-v2': {
            'dimensions': 768,
            'description': 'Higher quality embeddings, slower',
            'size': 'medium'
        },
        'paraphrase-multilingual-MiniLM-L12-v2': {
            'dimensions': 384,
            'description': 'Multilingual support',
            'size': 'small'
        }
    }
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.model_name = model_name
        self._model = None
        
        if model_name not in self.AVAILABLE_MODELS:
            logger.warning(f"Model {model_name} not in predefined list. Using anyway.")
    
    @property
    def model(self):
        """Lazy loading of the model."""
        if self._model is None:
            try:
                logger.info(f"Loading embedding model: {self.model_name}")
                self._model = SentenceTransformer(self.model_name)
                logger.info(f"Model loaded successfully. Embedding dimension: {self._model.get_sentence_embedding_dimension()}")
            except Exception as e:
                logger.error(f"Failed to load model {self.model_name}: {e}")
                raise
        return self._model
    
    def generate_embeddings(self, chunks: List[Dict[str, Any]], 
                          show_progress: bool = True) -> List[Dict[str, Any]]:
        """Generate embeddings for text chunks with metadata.
        
        Args:
            chunks: List of chunk dictionaries with 'text' key
            show_progress: Whether to show progress bar
            
        Returns:
            List of chunk dictionaries enhanced with embedding data
        """
        if not chunks:
            logger.warning("No chunks provided for embedding generation")
            return []
        
        # Extract text from chunks
        texts = [chunk.get('text', '') for chunk in chunks]
        
        try:
            logger.info(f"Generating embeddings for {len(texts)} chunks using {self.model_name}")
            embeddings = self.model.encode(
                texts, 
                show_progress_bar=show_progress,
                convert_to_numpy=True
            )
            
            # Enhance chunks with embedding data
            enhanced_chunks = []
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                enhanced_chunk = chunk.copy()
                enhanced_chunk.update({
                    'embedding': embedding.tolist(),
                    'embedding_model': self.model_name,
                    'embedding_dimension': len(embedding),
                    'embedding_id': f"{chunk.get('chunk_id', f'chunk_{i}')}_emb"
                })
                enhanced_chunks.append(enhanced_chunk)
            
            logger.info(f"Successfully generated {len(enhanced_chunks)} embeddings")
            return enhanced_chunks
            
        except Exception as e:
            logger.error(f"Failed to generate embeddings: {e}")
            raise
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model."""
        info = {
            'model_name': self.model_name,
            'embedding_dimension': self.model.get_sentence_embedding_dimension(),
            'is_loaded': self._model is not None
        }
        
        if self.model_name in self.AVAILABLE_MODELS:
            info.update(self.AVAILABLE_MODELS[self.model_name])
        
        return info

# Backward compatibility
_global_model = None

def get_embedding_model():
    """Legacy function for backward compatibility."""
    global _global_model
    if _global_model is None:
        _global_model = SentenceTransformer('all-MiniLM-L6-v2')
    return _global_model

def generate_embeddings(chunks: List[str]) -> List[List[float]]:
    """Legacy function for backward compatibility."""
    model = get_embedding_model()
    embeddings = model.encode(chunks, show_progress_bar=True).tolist()
    return embeddings
