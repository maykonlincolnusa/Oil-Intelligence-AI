import json

import httpx

from app.services.llm.base import LLMProvider


class OpenAICompatibleProvider(LLMProvider):
    def __init__(self, api_key: str, model: str = "gpt-4.1-mini") -> None:
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.openai.com/v1/responses"

    async def generate(self, prompt: str, system_prompt: str | None = None) -> str:
        payload: dict = {
            "model": self.model,
            "input": [
                {
                    "role": "user",
                    "content": [{"type": "input_text", "text": prompt}],
                }
            ],
            "max_output_tokens": 500,
        }
        if system_prompt:
            payload["instructions"] = system_prompt

        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(self.base_url, headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()

        if "output_text" in data and data["output_text"]:
            return str(data["output_text"])

        try:
            return json.dumps(data["output"])[:1200]
        except Exception:
            return ""
