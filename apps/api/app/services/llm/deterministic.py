import hashlib

from app.services.llm.base import LLMProvider


class DeterministicLLMProvider(LLMProvider):
    async def generate(self, prompt: str, system_prompt: str | None = None) -> str:
        digest = hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:8]
        return f"Deterministic AI placeholder response [{digest}]"
