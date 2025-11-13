import os
from typing import Optional
from openai import OpenAI
from ..prompt import SYSTEM_PROMPT


class OpenAIProvider:
    def __init__(self, model: Optional[str] = None):
        self.client = OpenAI()
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    def generate(self, query: str) -> str:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query},
        ]
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
        )
        return resp.choices[0].message.content.strip()
