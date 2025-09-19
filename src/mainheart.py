from core.file_handler import handle_file_upload
from core.text_normalizer import normalize_text
from pipeline.chunker import TextChunker
from pipeline.embedder import EmbeddingGenerator
from pipeline.vector_db import EnhancedVectorDB
import sys
import os
from pathlib import Path

# Add parent directory to path for imports
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))


def process_document(file_path: str, doc_id: str = None):
    if doc_id is None:
        doc_id = file_path.replace("/", "_").replace(".", "_")

    print(f"📂 Processing: {file_path}")

    # Step 1: Extract raw text
    raw_text = handle_file_upload(file_path)

    # Step 2: Normalize
    clean_text = normalize_text(raw_text)
    print(f"🧹 Cleaned text length: {len(clean_text)} chars")

    # Step 3: Chunk
    chunker = TextChunker()
    chunks_with_metadata = chunker.chunk_text(clean_text, doc_id=doc_id)
    chunks = [chunk['text'] for chunk in chunks_with_metadata]  # Extract text for compatibility
    print(f"✂️  Created {len(chunks)} chunks")

    # Step 4: Generate embeddings (optional if Chroma does it)
    # embeddings = generate_embeddings(chunks)  # Chroma can auto-embed

    # Step 5: Store in Vector DB
    db = EnhancedVectorDB()
    db.add_documents_with_metadata(chunks_with_metadata)

    print(f"✅ DONE. Doc '{doc_id}' ingested.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <file_path>")
        sys.exit(1)
    process_document(sys.argv[1])