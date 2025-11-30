"""Service for summarizing transcriptions."""

import logging
from openai import OpenAI
from backend.core.config import settings
from backend.core.constants import SYSTEM_MESSAGE, USER_PROMPT


logger = logging.getLogger(__name__)


def get_summarize(
    openai_client: OpenAI,
    transcription: str,
    model: str = None,
    system_message: str = None,
    user_prompt: str = None
) -> str:
    """Generate a summary of a transcription using GPT model.

    Args:
        openai_client (OpenAI): OpenAI client instance.
        transcription (str): Full transcription text of the video.
        model (str, optional): Model used for summarization.
            Defaults to settings.summarize_model.
        system_message (str, optional): System message with instructions.
            Defaults to SYSTEM_MESSAGE constant.
        user_prompt (str, optional): User request for summarization.
            Defaults to USER_PROMPT constant.

    Returns:
        str: Generated summary in Markdown format.
    """
    if model is None:
        model = settings.summarize_model
    if system_message is None:
        system_message = SYSTEM_MESSAGE
    if user_prompt is None:
        user_prompt = USER_PROMPT

    logger.info(f"[get_summarize] Generating summary with model {model}")

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"{user_prompt}\n\n{transcription}"}
    ]

    completions = openai_client.chat.completions.create(
        model=model,
        messages=messages
    )

    return completions.choices[0].message.content
