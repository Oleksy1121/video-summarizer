from video_summarizer.constants import SUMMARIZE_MODEL, SYSTEM_MESSAGE, USER_PROMPT

def get_summarize(openai, transcription, model=SUMMARIZE_MODEL, system_message=SYSTEM_MESSAGE, user_prompt=USER_PROMPT):
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"{user_prompt}\n\n{transcription}"}
    ]

    completions = openai.chat.completions.create(
        model=model,
        messages=messages
    )

    return completions.choices[0].message.content
