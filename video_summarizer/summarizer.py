from openai import OpenAI
from video_summarizer.constants import SUMMARIZE_MODEL, SYSTEM_MESSAGE, USER_PROMPT


def get_summarize(openai: OpenAI, transcription: str, model: str = SUMMARIZE_MODEL,
                  system_message: str = SYSTEM_MESSAGE, user_prompt: str = USER_PROMPT) -> str:
    """Generate a summary of a transcription using GPT model.

    Args:
        openai (OpenAI): OpenAI client instance.
        transcription (str): Full transcription text of the video.
        model (str, optional): Model used for summarization. Defaults to "gpt-4o-mini".
        system_message (Optional[str], optional): System message with instructions. Defaults to generic summarizer prompt.
        user_prompt (Optional[str], optional): User request for summarization. Defaults to generic request.

    Returns:
        str: Generated summary in Markdown format.
    """
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"{user_prompt}\n\n{transcription}"}
    ]

    completions = openai.chat.completions.create(
        model=model,
        messages=messages
    )

    return completions.choices[0].message.content
