import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")

    # Model configuration
    transcription_model: str = "whisper-1"
    summarize_model: str = "gpt-4o-mini"

    # Validation limits
    max_duration: int = 1800  # 30 minutes
    max_size: int = 30 * 1024 * 1024  # 30MB

    # File paths
    audio_directory: str = "data/audio"
    audio_filename: str = "data/audio/audio_from_video.mp3"

    class Config:
        env_file = ".env"


settings = Settings()
