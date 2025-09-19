from sentence_transformers import SentenceTransformer

_model = None

def get_embedding_model():
    global _model
    if _model is None:
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model

def generate_embeddings(chunks: list[str]) -> list[list[float]]:
    model = get_embedding_model()
    embeddings = model.encode(chunks, show_progress_bar=True).tolist()
    return embeddings