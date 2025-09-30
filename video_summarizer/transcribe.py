from openai import OpenAI
from video_summarizer.constants import AUDIO_FILENAME, TRANSCRIPTION_MODEL


def get_transcription(openai: OpenAI, audio_filename: str = AUDIO_FILENAME, 
                      model: str = TRANSCRIPTION_MODEL, verbose: bool = False) -> str:
    """Transcribe audio into text using OpenAI Whisper.

    Args:
        openai (OpenAI): OpenAI client instance.
        audio_filename (str, optional): Path to the audio file. Defaults to "audio/audio_from_video.mp3".
        model (str, optional): Transcription model name. Defaults to "whisper-1".
        verbose (bool, optional): Whether to print first 200 characters of transcription. Defaults to False.

    Returns:
        str: Transcribed text.
    """
    with open(audio_filename, 'rb') as audio_file:
        transcription = openai.audio.transcriptions.create(model=model, file=audio_file, response_format="text")
    print(transcription[:200]) if verbose else None
    return transcription