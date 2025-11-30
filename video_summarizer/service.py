import asyncio
import os
import glob
from dotenv import load_dotenv
from openai import OpenAI

from scripts.video_summarizer.download import download_audio, get_video_info, validate_video
from scripts.video_summarizer.transcribe import get_transcription
from scripts.video_summarizer.summarizer import get_summarize
from scripts.video_summarizer.constants import AUDIO_FILENAME


load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
openai = OpenAI(api_key=openai_api_key)


async def summarize_service(url: str, send_status):
    loop = asyncio.get_running_loop()
    await send_status("Validating URL...")

    is_valid, result = await loop.run_in_executor(None, validate_video, url)
    if not is_valid:
        await send_status(result)
        raise ValueError(result)

    try:
        await send_status("Downloading audio...")
        await loop.run_in_executor(None, download_audio, url)

        await send_status("Generate Transcription from audio file...")
        transcription = await loop.run_in_executor(None, lambda: get_transcription(openai=openai))

        await send_status("Generatng Summarize...")
        summary = await loop.run_in_executor(None, lambda: get_summarize(openai=openai, transcription=transcription))
    
    finally:
        audio_folder = os.path.dirname(AUDIO_FILENAME)
        for file_path in glob.glob(os.path.join(audio_folder, "*")):
            os.remove(file_path)

    await send_status("Finished!")
    return summary