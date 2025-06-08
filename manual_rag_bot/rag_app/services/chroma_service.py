import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
import os

_OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

_client = chromadb.HttpClient(host=os.getenv("CHROMA_HOST", "localhost"), port=int(os.getenv("CHROMA_PORT", "8001")))
_embedding_fn = OpenAIEmbeddingFunction(api_key=_OPENAI_API_KEY)
_collection = _client.get_or_create_collection("documents", embedding_function=_embedding_fn)


def add_document(doc_id: str, text: str) -> None:
    """Add document text to the Chroma collection."""
    _collection.add(documents=[text], ids=[doc_id])


def query(text: str, n_results: int = 3) -> list[str]:
    """Return the most similar documents' texts."""
    results = _collection.query(query_texts=[text], n_results=n_results)
    return results.get("documents", [[]])[0]
