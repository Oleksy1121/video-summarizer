"""Service for transcribing audio files."""

import logging
from openai import OpenAI
from backend.core.config import settings


logger = logging.getLogger(__name__)


def get_transcription(
    openai_client: OpenAI,
    audio_filename: str = None,
    model: str = None,
    verbose: bool = False
) -> str:
    """Transcribe audio into text using OpenAI Whisper.

    Args:
        openai_client (OpenAI): OpenAI client instance.
        audio_filename (str, optional): Path to the audio file.
            Defaults to settings.audio_filename.
        model (str, optional): Transcription model name.
            Defaults to settings.transcription_model.
        verbose (bool, optional): Whether to print first 200 characters of transcription.
            Defaults to False.

    Returns:
        str: Transcribed text.
    """
    if audio_filename is None:
        audio_filename = settings.audio_filename
    if model is None:
        model = settings.transcription_model

    logger.info(f"[get_transcription] Transcribing {audio_filename} with model {model}")

    with open(audio_filename, 'rb') as audio_file:
        transcription = openai_client.audio.transcriptions.create(
            model=model,
            file=audio_file,
            response_format="text"
        )

    if verbose:
        logger.info(f"[get_transcription] Preview: {transcription[:200]}")

    return transcription
