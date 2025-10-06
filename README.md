# Video Summarizer
An application for automatically summarizing YouTube videos in **Markdown format**.  
The project was built for educational purposes and evolved through two main versions:
1. **[Colab notebook – LLaMA 3.1 (quantized) + OpenAI Whisper](/notebooks/colab_video_summarizer_llama.ipynb)** – testing transcription and summarization with a local model.
2.  **[Jupyter notebook – GPT-4o-mini + OpenAI Whisper](/notebooks/jupyter_video_summarizer_gradio.ipynb)** - lightweight, cost-effective, and further developed as the final solution.

---
## Features
- Downloading audio from YouTube videos (**yt-dlp**)
- Transcribing audio with **Whisper-1**
- Generating summaries in structured **Markdown** with **GPT-4o-mini**
- Simple **Gradio** interface for testing
- Modular architecture with a dedicated **REST API (FastAPI)**

---
## Preview
Screenshot of the Gradio interface:

![Gradio Interface](/attachments/gradio.png)

---
## 🌐 Live Demo
You can try the deployed version of the project here:  
**[https://marcin-oleszczyk.pl/video-summarizer](https://marcin-oleszczyk.pl/video-summarizer)**

---
## Project Structure

``` bash
notebooks/
  colab_video_summarizer_llama.ipynb     # initial experiments with LLaMA
  jupyter_video_summarizer_gradio.ipynb  # prototype with Gradio and OpenAI
video_summarizer/
  constants.py     # model and prompt configuration
  download.py      # audio downloading
  transcribe.py    # audio transcription
  summarize.py     # text summarization
  utils.pu         # helpers functions like validation
```

---
## Technologies
- **Python, Jupyter/Colab**
- **yt-dlp** – audio extraction
- **OpenAI Whisper (whisper-1)** – transcription
- **GPT-4o-mini** – summarization
- **bitsandbytes** – LLaMA quantization (experimental)
- **Gradio** – UI prototype
- **FastAPI** – REST API

---
## Next Steps
- Export summaries to `.md` / `.pdf`
- Option to choose summarization models
- Multi-language transcription support