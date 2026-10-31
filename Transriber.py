import os
import time
from google import genai
from google.genai.errors import APIError
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# 1. Initialize Gemini Client
print("Initializing Gemini client...")
client = genai.Client()  # Uses GEMINI_API_KEY environment variable

# Use the requested audio file
audio_filename = "Sonargaon Janapath.m4a"

# 2. Upload file to Gemini API
print(f"Uploading {audio_filename} to Gemini...")
audio_file = client.files.upload(file=audio_filename)
print("Upload complete. Waiting for file to be processed by Gemini...")

# Poll file status until it is ACTIVE
while True:
    audio_file_status = client.files.get(name=audio_file.name)
    state = audio_file_status.state.name
    print(f"Current file state: {state}")
    if state == "ACTIVE":
        break
    elif state == "FAILED":
        raise RuntimeError("File processing failed on Gemini's servers.")
    time.sleep(5)

print("File is ready for analysis.")

def generate_with_fallback(contents, prompt_desc="content"):
    # Robust fallback list of models
    models = ["gemini-3.5-flash", "gemini-2.0-flash", "gemini-2.5-flash-lite"]
    
    for model in models:
        print(f"Generating {prompt_desc} using {model}...")
        # Try up to 3 times per model
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=contents,
                )
                text = response.text
                if not text or len(text.strip()) < 10:
                    print(f"Warning: Model {model} returned an empty or extremely short response.")
                    time.sleep(5)
                    continue
                return text
            except APIError as e:
                # Catch 429 (Resource/Quota Exhausted)
                if e.code == 429:
                    print(f"Rate limit exceeded (429) for {model}. Waiting 30 seconds to retry...")
                    time.sleep(30)
                    continue
                # Catch 503 (high demand) or other transient errors
                elif e.code in [503, 502, 504]:
                    print(f"Model {model} failed (Error {e.code}: {e.message}). Retrying in 5 seconds...")
                    time.sleep(5)
                    continue
                else:
                    print(f"API Error {e.code} for {model}: {e.message}. Trying next model...")
                    break
            except Exception as e:
                print(f"Unexpected error using model {model}: {e}")
                break
    raise RuntimeError("All fallback models failed to generate content.")

# 3. Generate transcript
transcript_prompt = """
You are an expert transcriber. Listen to the audio and transcribe it accurately.
If the audio is in Bangla, translate it to English or transcribe it in English.
Provide only the clean transcribed text without any extra chat.
"""
raw_transcript = generate_with_fallback([audio_file, transcript_prompt], "transcript")

# 4. Generate meeting minutes
minutes_prompt = f"""
You are an expert executive assistant. Analyze the meeting transcript provided below and generate formal Meeting Minutes using the following exact structure:

1. **Executive Summary**: A concise 2-3 sentence overview of the meeting's main purpose and outcome.
2. **Key Discussion Points**: Bullet points grouping the major topics discussed.
3. **Decisions Made**: A list of explicit agreements or final decisions reached.
4. **Action Items**: A Markdown table with columns: | Task | Assignee | Deadline / Status |.

Transcript:
---
{raw_transcript}
---
"""
minutes_text = generate_with_fallback(minutes_prompt, "meeting minutes")

# 5. Print and save output
print("\n=== MEETING MINUTES ===\n")
print(minutes_text)

# Save to Markdown file
with open("meeting_minutes.md", "w", encoding="utf-8") as f:
    f.write(minutes_text)

# Save raw transcript to text file
with open("transcript.txt", "w", encoding="utf-8") as f:
    f.write(raw_transcript)

# Cleanup the file from Gemini
print("\nCleaning up audio file from Gemini...")
try:
    client.files.delete(name=audio_file.name)
except Exception as e:
    print(f"Cleanup failed: {e}")

print("\nSaved minutes to meeting_minutes.md")
print("Saved transcript to transcript.txt")