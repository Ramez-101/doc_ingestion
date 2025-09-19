from core.file_handler import handle_file_upload
from core.text_normalizer import normalize_text
from pipeline.chunker import chunk_text
from pipeline.embedder import generate_embeddings
from pipeline.enhanced_vector_db import VectorDB
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
    chunks = chunk_text(clean_text)
    print(f"✂️  Created {len(chunks)} chunks")

    # Step 4: Generate embeddings (optional if Chroma does it)
    # embeddings = generate_embeddings(chunks)  # Chroma can auto-embed

    # Step 5: Store in Vector DB
    db = VectorDB()
    db.add_documents(chunks, doc_id)

    print(f"✅ DONE. Doc '{doc_id}' ingested.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <file_path>")
        sys.exit(1)
    process_document(sys.argv[1])