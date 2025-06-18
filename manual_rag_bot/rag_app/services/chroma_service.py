import chromadb
import os
import time
from typing import Dict
from . import openai_service

_CHROMA_HOST = os.getenv("CHROMA_HOST", "chromadb")
_CHROMA_PORT = int(os.getenv("CHROMA_PORT", "8000"))

_client = None
_collections: Dict[int, chromadb.api.models.Collection.Collection] = {}


def _ensure_connection() -> None:
    """Connect to ChromaDB lazily, retrying until it becomes available."""

    global _client

    attempts = 5
    last_exc: Exception | None = None
    for _ in range(attempts):
        try:
            if _client is None:
                _client = chromadb.HttpClient(host=_CHROMA_HOST, port=_CHROMA_PORT)
            return
        except Exception as exc:  # pragma: no cover - relies on external service
            last_exc = exc
            time.sleep(2)

    raise RuntimeError("Could not connect to ChromaDB service") from last_exc


def _get_collection(user_id: int):
    _ensure_connection()
    if user_id not in _collections:
        _collections[user_id] = _client.get_or_create_collection(
            f"documents_{user_id}",
            embedding_function=openai_service.create_embeddings,
        )
    return _collections[user_id]


def add_document(user_id: int, doc_id: str, text: str) -> None:
    """Add document text to the user's collection."""
    collection = _get_collection(user_id)
    collection.add(documents=[text], ids=[doc_id])


def query(user_id: int, text: str, n_results: int = 3) -> list[str]:
    """Return the most similar documents' texts for a user."""
    collection = _get_collection(user_id)
    results = collection.query(query_texts=[text], n_results=n_results)
    return results.get("documents", [[]])[0]
