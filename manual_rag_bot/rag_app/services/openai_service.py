import os
import openai

_CLIENT = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def _no_api_key() -> bool:
    """Return True if the OpenAI API key is not configured."""
    return not _CLIENT.api_key


def ask_openai(prompt: str) -> str:
    """Simple wrapper around OpenAI ChatCompletion."""
    if _no_api_key():
        return "OPENAI_API_KEY が設定されていません。"

    response = _CLIENT.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "あなたは親切なアシスタントです。"},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content


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

    res = _CLIENT.embeddings.create(
        model="text-embedding-3-small",
        input=texts,
    )
    return [record.embedding for record in res.data]

