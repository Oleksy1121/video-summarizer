from openai import OpenAI
import os
from dotenv import load_dotenv
from video_summarizer.transcribe import get_transcription

load_dotenv()
open_ai_api_key = os.getenv("OPENAI_API_KEY")
openai = OpenAI()

get_transcription(openai=openai, verbose=True)
