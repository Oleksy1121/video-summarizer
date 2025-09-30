import os
import subprocess
from video_summarizer.constants import AUDIO_FILENAME

def download_audio(url, audio_filename=AUDIO_FILENAME):
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
