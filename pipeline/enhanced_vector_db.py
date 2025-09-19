import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict, Any, Optional
import logging
import json

logger = logging.getLogger(__name__)

class EnhancedVectorDB:
    """Enhanced vector database with metadata storage and improved querying."""
    
    def __init__(self, collection_name: str = "documents", 
                 persist_dir: str = "./chroma_db",
                 embedding_model: str = "all-MiniLM-L6-v2"):
        self.collection_name = collection_name
        self.persist_dir = persist_dir
        self.embedding_model = embedding_model
        
        try:
            self.client = chromadb.PersistentClient(path=persist_dir)
            self.collection = self.client.get_or_create_collection(
                name=collection_name,
                embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(
                    model_name=embedding_model
                )
            )
            logger.info(f"Connected to ChromaDB collection: {collection_name}")
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {e}")
            raise
    
    def add_documents_with_metadata(self, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Add documents with full metadata to the vector database.
        
        Args:
            chunks: List of chunk dictionaries with text and metadata
            
        Returns:
            Dictionary with operation results and references
        """
        if not chunks:
            logger.warning("No chunks provided for storage")
            return {"status": "error", "message": "No chunks provided"}
        
        try:
            # Prepare data for ChromaDB
            documents = []
            ids = []
            metadatas = []
            
            for chunk in chunks:
                documents.append(chunk['text'])
                ids.append(chunk['chunk_id'])
                
                # Prepare metadata (ChromaDB doesn't store complex objects)
                metadata = {
                    'doc_id': chunk.get('doc_id', ''),
                    'chunk_index': chunk.get('chunk_index', 0),
                    'char_count': chunk.get('char_count', 0),
                    'word_count': chunk.get('word_count', 0),
                    'chunk_size_config': chunk.get('chunk_size_config', 0),
                    'chunk_overlap_config': chunk.get('chunk_overlap_config', 0),
                    'embedding_model': chunk.get('embedding_model', self.embedding_model),
                    'embedding_dimension': chunk.get('embedding_dimension', 0)
                }
                metadatas.append(metadata)
            
            # Add to ChromaDB
            self.collection.add(
                documents=documents,
                ids=ids,
                metadatas=metadatas
            )
            
            result = {
                "status": "success",
                "chunks_stored": len(chunks),
                "collection_name": self.collection_name,
                "embedding_references": ids,
                "doc_ids": list(set(chunk.get('doc_id') for chunk in chunks if chunk.get('doc_id')))
            }
            
            logger.info(f"Successfully stored {len(chunks)} chunks in vector database")
            return result
            
        except Exception as e:
            logger.error(f"Failed to add documents to vector database: {e}")
            return {"status": "error", "message": str(e)}
    
    def query_with_metadata(self, query_text: str, n_results: int = 5, 
                           doc_id_filter: Optional[str] = None) -> Dict[str, Any]:
        """Query the vector database with enhanced results including metadata.
        
        Args:
            query_text: Text to search for
            n_results: Number of results to return
            doc_id_filter: Optional filter by document ID
            
        Returns:
            Dictionary with query results and metadata
        """
        try:
            where_clause = None
            if doc_id_filter:
                where_clause = {"doc_id": doc_id_filter}
            
            results = self.collection.query(
                query_texts=[query_text],
                n_results=n_results,
                where=where_clause,
                include=['documents', 'metadatas', 'distances']
            )
            
            # Format results
            formatted_results = {
                "query": query_text,
                "total_results": len(results['documents'][0]) if results['documents'] else 0,
                "results": []
            }
            
            if results['documents'] and results['documents'][0]:
                for i in range(len(results['documents'][0])):
                    result_item = {
                        "chunk_id": results['ids'][0][i],
                        "text": results['documents'][0][i],
                        "similarity_score": 1 - results['distances'][0][i],  # Convert distance to similarity
                        "metadata": results['metadatas'][0][i] if results['metadatas'] else {}
                    }
                    formatted_results["results"].append(result_item)
            
            logger.info(f"Query returned {formatted_results['total_results']} results")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Failed to query vector database: {e}")
            return {"status": "error", "message": str(e)}
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the collection."""
        try:
            count = self.collection.count()
            return {
                "collection_name": self.collection_name,
                "total_documents": count,
                "embedding_model": self.embedding_model,
                "persist_dir": self.persist_dir
            }
        except Exception as e:
            logger.error(f"Failed to get collection stats: {e}")
            return {"status": "error", "message": str(e)}

# Backward compatibility class
class VectorDB:
    """Legacy VectorDB class for backward compatibility."""
    
    def __init__(self, collection_name="documents", persist_dir="./chroma_db"):
        self.enhanced_db = EnhancedVectorDB(collection_name, persist_dir)
    
    def add_documents(self, chunks: List[str], doc_id: str):
        """Legacy method for backward compatibility."""
        # Convert simple chunks to enhanced format
        enhanced_chunks = []
        for i, chunk in enumerate(chunks):
            chunk_data = {
                "text": chunk,
                "chunk_id": f"{doc_id}_{i}",
                "doc_id": doc_id,
                "chunk_index": i,
                "char_count": len(chunk),
                "word_count": len(chunk.split())
            }
            enhanced_chunks.append(chunk_data)
        
        result = self.enhanced_db.add_documents_with_metadata(enhanced_chunks)
        if result["status"] == "success":
            print(f"✅ Added {len(chunks)} chunks to vector DB.")
        else:
            print(f"❌ Failed to add chunks: {result['message']}")
    
    def query(self, query_text: str, n_results=5):
        """Legacy method for backward compatibility."""
        return self.enhanced_db.collection.query(query_texts=[query_text], n_results=n_results)
