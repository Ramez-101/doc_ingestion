from core.file_handler import handle_file_upload
from core.text_normalizer import normalize_text
from pipeline.enhanced_chunker import TextChunker
from pipeline.enhanced_embedder import EmbeddingGenerator
from pipeline.enhanced_vector_db import EnhancedVectorDB
import sys
import logging
from typing import Dict, Any, List
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NLPPipeline:
    """Complete NLP preprocessing pipeline with chunking, embeddings, and vector storage."""
    
    def __init__(self, 
                 chunk_size: int = 500, 
                 chunk_overlap: int = 50,
                 embedding_model: str = 'all-MiniLM-L6-v2',
                 collection_name: str = "documents",
                 persist_dir: str = "./chroma_db"):
        
        self.chunker = TextChunker(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        self.embedder = EmbeddingGenerator(model_name=embedding_model)
        self.vector_db = EnhancedVectorDB(
            collection_name=collection_name, 
            persist_dir=persist_dir,
            embedding_model=embedding_model
        )
        
        logger.info(f"NLP Pipeline initialized with:")
        logger.info(f"  - Chunk size: {chunk_size}, overlap: {chunk_overlap}")
        logger.info(f"  - Embedding model: {embedding_model}")
        logger.info(f"  - Vector DB: {collection_name} at {persist_dir}")
    
    def process_document(self, file_path: str, doc_id: str = None) -> Dict[str, Any]:
        """
        Complete document processing pipeline.
        
        Args:
            file_path: Path to the document file
            doc_id: Optional document identifier
            
        Returns:
            Dictionary containing:
            - clean_text: Normalized text
            - chunks: List of text chunks with metadata
            - embeddings_reference: Reference to stored embeddings
            - vector_db_info: Information about vector database storage
            - processing_stats: Statistics about the processing
        """
        if doc_id is None:
            doc_id = Path(file_path).stem.replace(" ", "_")
        
        logger.info(f"📂 Processing document: {file_path}")
        
        try:
            # Step 1: Extract raw text from file
            logger.info("Step 1: Extracting text from file...")
            raw_text = handle_file_upload(file_path)
            
            # Step 2: Normalize text
            logger.info("Step 2: Normalizing text...")
            clean_text = normalize_text(raw_text)
            logger.info(f"🧹 Text normalized: {len(clean_text)} characters")
            
            # Step 3: Create text chunks with metadata
            logger.info("Step 3: Creating text chunks...")
            chunks = self.chunker.chunk_text(clean_text, doc_id=doc_id)
            logger.info(f"✂️  Created {len(chunks)} chunks")
            
            # Step 4: Generate embeddings for chunks
            logger.info("Step 4: Generating embeddings...")
            chunks_with_embeddings = self.embedder.generate_embeddings(chunks)
            logger.info(f"🔢 Generated embeddings for {len(chunks_with_embeddings)} chunks")
            
            # Step 5: Store in vector database
            logger.info("Step 5: Storing in vector database...")
            storage_result = self.vector_db.add_documents_with_metadata(chunks_with_embeddings)
            
            # Prepare return data
            result = {
                "status": "success",
                "file_path": file_path,
                "doc_id": doc_id,
                "clean_text": clean_text,
                "chunks": chunks_with_embeddings,
                "embeddings_reference": {
                    "collection_name": self.vector_db.collection_name,
                    "chunk_ids": [chunk["chunk_id"] for chunk in chunks_with_embeddings],
                    "embedding_model": self.embedder.model_name,
                    "embedding_dimension": chunks_with_embeddings[0]["embedding_dimension"] if chunks_with_embeddings else 0
                },
                "vector_db_info": storage_result,
                "processing_stats": {
                    "original_text_length": len(raw_text),
                    "clean_text_length": len(clean_text),
                    "total_chunks": len(chunks_with_embeddings),
                    "avg_chunk_size": sum(chunk["char_count"] for chunk in chunks_with_embeddings) / len(chunks_with_embeddings) if chunks_with_embeddings else 0,
                    "chunk_size_config": self.chunker.chunk_size,
                    "chunk_overlap_config": self.chunker.chunk_overlap
                }
            }
            
            logger.info(f"✅ Document processing completed successfully!")
            logger.info(f"   - Original text: {len(raw_text)} chars")
            logger.info(f"   - Clean text: {len(clean_text)} chars") 
            logger.info(f"   - Chunks created: {len(chunks_with_embeddings)}")
            logger.info(f"   - Embeddings stored in: {self.vector_db.collection_name}")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Error processing document {file_path}: {e}")
            return {
                "status": "error",
                "file_path": file_path,
                "doc_id": doc_id,
                "error": str(e)
            }
    
    def query_documents(self, query_text: str, n_results: int = 5, 
                       doc_id_filter: str = None) -> Dict[str, Any]:
        """Query the processed documents."""
        logger.info(f"🔍 Querying: '{query_text}' (top {n_results} results)")
        return self.vector_db.query_with_metadata(query_text, n_results, doc_id_filter)
    
    def get_pipeline_stats(self) -> Dict[str, Any]:
        """Get statistics about the pipeline and stored documents."""
        db_stats = self.vector_db.get_collection_stats()
        model_info = self.embedder.get_model_info()
        
        return {
            "chunker_config": {
                "chunk_size": self.chunker.chunk_size,
                "chunk_overlap": self.chunker.chunk_overlap,
                "separators": self.chunker.separators
            },
            "embedder_info": model_info,
            "vector_db_stats": db_stats
        }

# Backward compatibility function
def process_document(file_path: str, doc_id: str = None):
    """Legacy function for backward compatibility with existing mainheart.py"""
    pipeline = NLPPipeline()
    result = pipeline.process_document(file_path, doc_id)
    
    if result["status"] == "success":
        print(f"📂 Processing: {file_path}")
        print(f"🧹 Cleaned text length: {result['processing_stats']['clean_text_length']} chars")
        print(f"✂️  Created {result['processing_stats']['total_chunks']} chunks")
        print(f"✅ DONE. Doc '{doc_id}' ingested.")
    else:
        print(f"❌ ERROR processing {file_path}: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python enhanced_pipeline.py <file_path> [doc_id]")
        print("Example: python enhanced_pipeline.py document.pdf my_document")
        sys.exit(1)
    
    file_path = sys.argv[1]
    doc_id = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Create and run pipeline
    pipeline = NLPPipeline()
    result = pipeline.process_document(file_path, doc_id)
    
    # Print results
    if result["status"] == "success":
        print("\n" + "="*50)
        print("📊 PROCESSING RESULTS")
        print("="*50)
        print(f"Document ID: {result['doc_id']}")
        print(f"Original text length: {result['processing_stats']['original_text_length']:,} characters")
        print(f"Clean text length: {result['processing_stats']['clean_text_length']:,} characters")
        print(f"Total chunks: {result['processing_stats']['total_chunks']}")
        print(f"Average chunk size: {result['processing_stats']['avg_chunk_size']:.1f} characters")
        print(f"Embedding model: {result['embeddings_reference']['embedding_model']}")
        print(f"Embedding dimension: {result['embeddings_reference']['embedding_dimension']}")
        print(f"Vector DB collection: {result['embeddings_reference']['collection_name']}")
        print("="*50)
    else:
        print(f"\n❌ Processing failed: {result.get('error', 'Unknown error')}")
