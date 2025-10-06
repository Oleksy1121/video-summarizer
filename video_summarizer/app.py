import os
from dotenv import load_dotenv
from openai import OpenAI
import glob
import logging

from video_summarizer.download import download_audio
from video_summarizer.transcribe import get_transcription
from video_summarizer.summarizer import get_summarize
from video_summarizer.utils import validate_video
from video_summarizer.constants import AUDIO_FILENAME, VIDEO_URL


# --- Logging configuration ---
logging.basicConfig(
    level=logging.ERROR, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI()


def summarize_service(url, openai_client=openai_client):
    logger.info(f"Starting summarization process for URL: {url}")
    is_valid, result = validate_video(url)

    if is_valid:
        logger.info("Video validation successful")
    if not is_valid:
        logger.info(f"Invalid video link: {result}")
        raise ValueError(result)
    
    try:
        logger.info("Downloading audio from the video...")
        download_audio(url)

        logger.info("Transcribing audio...")
        transcription = get_transcription(openai=openai_client)

        logger.info("Generating summary based on transcription...")
        summarize = get_summarize(openai=openai_client, transcription=transcription)
        logger.info("Summarization completed successfully.")
    
    except Exception as e:
        logger.info(f"An error occured during processing: {e}")

    finally:
        logger.info("Cleaning up temporary files...")
        audio_folder = os.path.dirname(AUDIO_FILENAME)
        for file_path in glob.glob(os.path.join(audio_folder, "*")):
            os.remove(file_path)
        logger.debug("Temporary files deleted.")

    return summarize

result = summarize_service(VIDEO_URL)
print(result)
