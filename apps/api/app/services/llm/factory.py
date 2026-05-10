from app.core.config import get_settings
from app.services.llm.base import LLMProvider
from app.services.llm.deterministic import DeterministicLLMProvider
from app.services.llm.openai_provider import OpenAICompatibleProvider


def get_llm_provider() -> LLMProvider:
    settings = get_settings()
    if settings.openai_api_key:
        return OpenAICompatibleProvider(api_key=settings.openai_api_key)
    return DeterministicLLMProvider()
