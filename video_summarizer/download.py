import os
import subprocess
import logging
from video_summarizer.constants import AUDIO_FILENAME


def download_audio(url: str, audio_filename: str = AUDIO_FILENAME) -> None:
    """Download audio from a URL video using yt-dlp.

    Args:
        url (str): Video URL.
        audio_filename (str, optional): Path to save the downloaded audio file. Defaults to "audio/audio_from_video.mp3".

    Returns:
        None
    """
    if os.path.exists(audio_filename):
        logging.info(f"[download_audio] Downloading audio from: {url} -> {audio_filename}")
        os.remove(audio_filename)
        # print("Old audio file has been deleted.")
        
    result = subprocess.run([
        "yt-dlp",
        "-x",                        # only audio
        "--audio-format", "mp3",     # convert to mp3
        "--force-overwrites",        # forve override file
        "-o", audio_filename,        # save file
        url
    ], capture_output=True, text=True)

    logging.info(f"[download_audio] returncode={result.returncode}")
    logging.info(f"[download_audio] stdout={result.stdout[:300]}")
    logging.info(f"[download_audio] stderr={result.stderr}")
