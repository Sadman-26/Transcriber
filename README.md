# Audio Transcriber & Meeting Minutes Generator

An automated AI tool powered by Google Gemini that transcribes audio recordings (including Bangla to English translation) and synthesizes structured, executive-ready meeting minutes.

## Features

- **Audio Upload & Processing**: Uploads audio files to Gemini's File API and waits for processing readiness.
- **Multilingual Transcription**: Generates clean transcriptions, with automatic translation to English for Bangla audio.
- **Structured Minutes Extraction**:
  - Executive Summary
  - Key Discussion Points
  - Decisions Made
  - Action Items Table (Task, Assignee, Deadline / Status)
- **Automatic Cleanup**: Deletes uploaded audio files from Gemini storage after processing.
- **Resilient Fallback Mechanism**: Tries multiple Gemini models (`gemini-3.5-flash`, `gemini-2.0-flash`, `gemini-2.5-flash-lite`) with retry logic for rate limits and transient errors.

## Prerequisites

- Python 3.10+
- A Google Gemini API key

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/Sadman-26/Transcriber.git
cd Transcriber
```

### 2. Set Up Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env` and add your Gemini API key:
```bash
cp .env.example .env
```
Edit `.env`:
```env
GEMINI_API_KEY="your_api_key_here"
```

### 5. Run the Script
Place your audio file in the project folder and update `audio_filename` in `Transriber.py`, then run:
```bash
python Transriber.py
```

Generated outputs:
- `transcript.txt` — Raw transcript of the audio
- `meeting_minutes.md` — Formal meeting minutes in Markdown
