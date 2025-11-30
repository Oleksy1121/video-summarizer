# Video Summarizer

An application for automatically summarizing YouTube videos in **Markdown format** using **OpenAI Whisper** and **GPT-4o-mini**.

---

## 🚀 Live Demo

**Frontend:** [https://marcin-oleszczyk.pl/video-summarizer](https://marcin-oleszczyk.pl/video-summarizer)  
**API Docs:** [https://video-summarizer-backend-202366413188.europe-west4.run.app/docs](https://video-summarizer-backend-202366413188.europe-west4.run.app/docs)

---

## Features

- Audio extraction from YouTube videos (**yt-dlp**)
- Transcription with **OpenAI Whisper-1**
- Summarization with **GPT-4o-mini** in structured Markdown
- REST API built with **FastAPI**
- Rate limiting (2 requests per 4 hours)
- Dockerized deployment on **GCP Cloud Run**

---

## Project Structure
```bash
backend/
├── api/          # API routes and dependencies
├── core/         # Configuration
├── models/       # Pydantic schemas
├── services/     # Business logic (download, transcribe, summarize)
├── utils/        # Validators and helpers
└── main.py       # FastAPI entry point

notebooks/        # Initial prototypes
Dockerfile        # Backend containerization
docker-compose.yml
deploy.sh         # GCP deployment script
```

---

## Technologies

**Backend:** Python 3.12, FastAPI, yt-dlp, OpenAI (Whisper-1, GPT-4o-mini)  
**Infrastructure:** Docker, GCP Cloud Run, Secret Manager  
**Development:** Jupyter, Gradio (prototyping)

---

## Getting Started

### Local Development
```bash
# Clone repository
git clone https://github.com/Oleksy1121/video-summarizer.git
cd video-summarizer

# Create .env file
echo "OPENAI_API_KEY=your_key_here" > .env

# Run with Docker
docker-compose up --build

# Access API at http://localhost:8000/docs
```

### Deploy to GCP
```bash
./deploy.sh
```

---

## API Usage

**Endpoint:** `POST /api/v1/summarize`
```json
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

**Response:**
```json
{
  "summary": "# Video Title\n\n## Summary..."
}
```

---

## Author

**Marcin Oleszczyk**  
Portfolio: [marcin-oleszczyk.pl](https://marcin-oleszczyk.pl) | GitHub: [@Oleksy1121](https://github.com/Oleksy1121)