"""Service for downloading audio from video URLs."""

import os
import subprocess
import logging
from backend.core.config import settings


logger = logging.getLogger(__name__)


def download_audio(url: str, audio_filename: str = None) -> None:
    """Download audio from a URL video using yt-dlp.

    Args:
        url (str): Video URL.
        audio_filename (str, optional): Path to save the downloaded audio file.
            Defaults to settings.audio_filename.

    Returns:
        None
    """
    if audio_filename is None:
        audio_filename = settings.audio_filename


    # Ensure directory exists
    os.makedirs(os.path.dirname(audio_filename), exist_ok=True)
    print(audio_filename)

    if os.path.exists(audio_filename):
        logger.info(f"[download_audio] Removing existing file: {audio_filename}")
        os.remove(audio_filename)

    logger.info(f"[download_audio] Downloading audio from: {url} -> {audio_filename}")

    result = subprocess.run([
        "yt-dlp",
        "-x",                        # only audio
        "--audio-format", "mp3",     # convert to mp3
        "--force-overwrites",        # force override file
        "-o", audio_filename,        # save file
        url
    ], capture_output=True, text=True)

    logger.info(f"[download_audio] returncode={result.returncode}")
    logger.debug(f"[download_audio] stdout={result.stdout[:300]}")
    logger.debug(f"[download_audio] stderr={result.stderr}")

    if result.returncode != 0:
        raise RuntimeError(f"Failed to download audio: {result.stderr}")
