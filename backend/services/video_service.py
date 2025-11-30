"""Main video summarization service orchestrating the entire workflow."""

import os
import glob
import logging
from openai import OpenAI
from backend.core.config import settings
from backend.services.download_service import download_audio
from backend.services.transcribe_service import get_transcription
from backend.services.summarize_service import get_summarize
from backend.utils.validators import validate_video


logger = logging.getLogger(__name__)


def summarize_video(url: str, openai_client: OpenAI) -> str:
    """
    Complete workflow for summarizing a video from URL.

    Args:
        url (str): Video URL to summarize.
        openai_client (OpenAI): OpenAI client instance.

    Returns:
        str: Video summary in Markdown format.

    Raises:
        ValueError: If video validation fails.
        RuntimeError: If any step in the process fails.
    """
    logger.info(f"Starting summarization process for URL: {url}")

    # Validate video
    is_valid, result = validate_video(url)
    if not is_valid:
        logger.error(f"Invalid video link: {result}")
        raise ValueError(result)

    logger.info("Video validation successful")

    try:
        # Download audio
        logger.info("Downloading audio from the video...")
        download_audio(url)

        # Transcribe audio
        logger.info("Transcribing audio...")
        transcription = get_transcription(openai_client=openai_client)

        # Generate summary
        logger.info("Generating summary based on transcription...")
        summary = get_summarize(openai_client=openai_client, transcription=transcription)
        logger.info("Summarization completed successfully.")

        return summary

    except Exception as e:
        logger.error(f"An error occurred during processing: {e}", exc_info=True)
        raise

    finally:
        # Cleanup temporary files
        logger.info("Cleaning up temporary files...")
        audio_folder = settings.audio_directory
        if os.path.exists(audio_folder):
            for file_path in glob.glob(os.path.join(audio_folder, "*")):
                try:
                    os.remove(file_path)
                    logger.debug(f"Deleted temporary file: {file_path}")
                except Exception as e:
                    logger.warning(f"Failed to delete {file_path}: {e}")
