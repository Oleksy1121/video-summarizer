import os
import subprocess
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
        os.remove(audio_filename)
        # print("Old audio file has been deleted.")
        
    subprocess.run([
        "yt-dlp",
        "-x",                        # only audio
        "--audio-format", "mp3",     # convert to mp3
        "--force-overwrites",        # forve override file
        "-o", audio_filename,        # save file
        url
    ])
