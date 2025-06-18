import os
import struct
import hashlib
import logging
import openai

_CLIENT = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class OpenAIEmbeddingFunction:
    """Embedding function compatible with ChromaDB."""

    def __call__(self, input: list[str]) -> list[list[float]]:
        if _no_api_key():
            raise RuntimeError("OPENAI_API_KEY が設定されていません。")

        try:
            res = _CLIENT.embeddings.create(
                model="text-embedding-3-small",
                input=input,
            )
            return [record.embedding for record in res.data]
        except Exception as exc:  # pragma: no cover - network errors
            logging.warning("OpenAI embedding failed: %s", exc)
            return [simple_embedding(text) for text in input]


EMBEDDING_FUNCTION = OpenAIEmbeddingFunction()


def simple_embedding(text: str, dim: int = 1536) -> list[float]:
    """Return a deterministic embedding using SHA256 hashing."""
    digest = hashlib.sha256(text.encode("utf-8")).digest()
    needed = dim * 4
    data = (digest * ((needed + len(digest) - 1) // len(digest)))[:needed]
    return [struct.unpack("<I", data[i : i + 4])[0] / 0xFFFFFFFF for i in range(0, needed, 4)]


def _no_api_key() -> bool:
    """Return True if the OpenAI API key is not configured."""
    return not _CLIENT.api_key


def ask_openai(prompt: str) -> str:
    """Simple wrapper around OpenAI ChatCompletion."""
    if _no_api_key():
        return "OPENAI_API_KEY が設定されていません。"

    try:
        response = _CLIENT.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "あなたは親切なアシスタントです。"},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content
    except Exception as exc:  # pragma: no cover - network errors
        logging.warning("OpenAI completion failed: %s", exc)
        return "(OpenAI API error)"


def ask_with_context(question: str, context: str) -> str:
    """Ask OpenAI with additional contextual information."""
    prompt = (
        "以下のコンテキストを参考に質問に答えてください。\n\n"
        f"コンテキスト:\n{context}\n\n質問:{question}"
    )
    return ask_openai(prompt)


def create_embeddings(texts: list[str]) -> list[list[float]]:
    """Return embeddings for the provided texts."""
    if _no_api_key():
        raise RuntimeError("OPENAI_API_KEY が設定されていません。")

    try:
        res = _CLIENT.embeddings.create(
            model="text-embedding-3-small",
            input=texts,
        )
        return [record.embedding for record in res.data]
    except Exception as exc:  # pragma: no cover - network errors
        logging.warning("OpenAI embedding failed: %s", exc)
        return [simple_embedding(text) for text in texts]

