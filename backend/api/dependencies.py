"""FastAPI dependency injection for shared resources."""

from functools import lru_cache
from openai import OpenAI
from backend.core.config import settings


@lru_cache()
def get_settings():
    """Get cached settings instance."""
    return settings


def get_openai_client() -> OpenAI:
    """
    Get OpenAI client instance.

    Returns:
        OpenAI: Configured OpenAI client.
    """
    return OpenAI(api_key=settings.openai_api_key)
