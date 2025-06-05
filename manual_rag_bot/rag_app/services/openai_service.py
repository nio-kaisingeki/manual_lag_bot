import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_openai(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "あなたは親切なアシスタントです。"},
            {"role": "user", "content": prompt},
        ],
    )
    return response["choices"][0]["message"]["content"]