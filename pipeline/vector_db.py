import chromadb
from chromadb.utils import embedding_functions


class VectorDB:
    def __init__(self, collection_name="documents", persist_dir="./chroma_db"):
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name="all-MiniLM-L6-v2"
            )
        )

    def add_documents(self, chunks: list[str], doc_id: str):
        ids = [f"{doc_id}_{i}" for i in range(len(chunks))]
        self.collection.add(
            documents=chunks,
            ids=ids
        )
        print(f"✅ Added {len(chunks)} chunks to vector DB.")

    def query(self, query_text: str, n_results=5):
        return self.collection.query(query_texts=[query_text], n_results=n_results)