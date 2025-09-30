
from video_summarizer.constants import AUDIO_FILENAME, TRANSCRIPTION_MODEL

def get_transcription(openai, audio_filename=AUDIO_FILENAME, model=TRANSCRIPTION_MODEL, verbose=False):
    with open(audio_filename, 'rb') as audio_file:
        transcription = openai.audio.transcriptions.create(model=model, file=audio_file, response_format="text")
    print(transcription[:200]) if verbose else None
    return transcription