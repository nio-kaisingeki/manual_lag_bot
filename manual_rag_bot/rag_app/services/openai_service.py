import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


def ask_openai(prompt: str) -> str:
    """Simple wrapper around OpenAI ChatCompletion."""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "あなたは親切なアシスタントです。"},
            {"role": "user", "content": prompt},
        ],
    )
    return response["choices"][0]["message"]["content"]


def ask_with_context(question: str, context: str) -> str:
    """Ask OpenAI with additional contextual information."""
    prompt = (
        "以下のコンテキストを参考に質問に答えてください。\n\n" f"コンテキスト:\n{context}\n\n質問:{question}"
    )
    return ask_openai(prompt)
