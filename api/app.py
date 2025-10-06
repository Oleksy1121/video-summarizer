from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from openai import OpenAI

from video_summarizer.download import download_audio
from video_summarizer.transcribe import get_transcription
from video_summarizer.summarizer import get_summarize


load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
openai = OpenAI()


app = FastAPI()


class VideoURL(BaseModel):
    url: str


@app.post("/summarize")
def summarize_video(video: VideoURL):
    download_audio(video.url)
    transcription = get_transcription(openai=openai)
    summarize = get_summarize(openai=openai, transcription=transcription)
    return {"summary": summarize}

