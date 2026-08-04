import os

from .groq import GroqProvider
from .ollama import OllamaProvider


def get_provider():
    provider = os.getenv("LLM_PROVIDER", "ollama").lower()

    providers = {
        "ollama": OllamaProvider,
        "groq": GroqProvider,
    }

    if provider not in providers:
        raise ValueError(
            f"LLM_PROVIDER '{provider}' não é suportado."
        )

    return providers[provider]()