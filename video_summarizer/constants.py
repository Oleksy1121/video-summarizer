TRANSCRIPTION_MODEL = 'whisper-1'
SUMMARIZE_MODEL = "gpt-4o-mini"

VIDEO_URL = "https://www.youtube.com/watch?v=TMkoX1kfyDs&t"
AUDIO_FILENAME = 'data/audio/audio_from_wideo.mp3'

SYSTEM_MESSAGE = "You are an assistant that summarizes YouTube videos by highlighting the most important points and events, in clear Markdown format."
USER_PROMPT = f"Below is the transcript of a YouTube video. Please write a summary describing the key moments, main ideas, and highlights in a structured way (using bullet points or short sections)."