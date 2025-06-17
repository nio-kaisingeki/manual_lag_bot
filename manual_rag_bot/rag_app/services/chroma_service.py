import chromadb
import os
import time
from . import openai_service

_CHROMA_HOST = os.getenv("CHROMA_HOST", "chromadb")
_CHROMA_PORT = int(os.getenv("CHROMA_PORT", "8000"))

_client = None
_collection = None


def _ensure_connection() -> None:
    """Connect to ChromaDB lazily, retrying until it becomes available."""

    global _client, _collection
    if _collection is not None:
        return

    attempts = 5
    last_exc: Exception | None = None
    for _ in range(attempts):
        try:
            if _client is None:
                _client = chromadb.HttpClient(host=_CHROMA_HOST, port=_CHROMA_PORT)
            _collection = _client.get_or_create_collection(
                "documents",
                embedding_function=openai_service.create_embeddings,
            )
            return
        except Exception as exc:  # pragma: no cover - relies on external service
            last_exc = exc
            time.sleep(2)

    raise RuntimeError("Could not connect to ChromaDB service") from last_exc


def add_document(doc_id: str, text: str) -> None:
    """Add document text to the Chroma collection."""
    _ensure_connection()
    embedding = openai_service.create_embeddings([text])[0]
    _collection.add(documents=[text], ids=[doc_id], embeddings=[embedding])


def query(text: str, n_results: int = 3) -> list[str]:
    """Return the most similar documents' texts."""
    _ensure_connection()
    embedding = openai_service.create_embeddings([text])[0]
    results = _collection.query(query_embeddings=[embedding], n_results=n_results)
    return results.get("documents", [[]])[0]
