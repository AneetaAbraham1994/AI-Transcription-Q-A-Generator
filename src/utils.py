import os
import tempfile
import json
from fastapi import UploadFile
from dotenv import load_dotenv
from groq import Groq
import google.generativeai as genai

# Load environment variables
load_dotenv()

# API Keys
groq_api_key = os.getenv("GROQ_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not groq_api_key or not gemini_api_key:
    raise ValueError("Missing API Keys: Ensure GROQ_API_KEY and GEMINI_API_KEY are set.")

# Initialize APIs
groq_client = Groq(api_key=groq_api_key)
genai.configure(api_key=gemini_api_key)

def save_audio_temp(file: UploadFile) -> str:
    """Save uploaded audio file temporarily."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".m4a") as tmp_file:
        tmp_file.write(file.file.read())
        return tmp_file.name

def delete_temp_file(file_path: str):
    """Delete a temporary file after processing."""
    os.unlink(file_path)

def generate_transcription(file_path: str) -> str:
    """Generate transcription using Groq Whisper."""
    with open(file_path, "rb") as f:
        transcription = groq_client.audio.transcriptions.create(
            file=f, model="whisper-large-v3", response_format="json",
            language="en", temperature=0.0
        )
    return transcription.text

def generate_qa(transcription: str) -> dict:
    """Generate a structured Q&A session based on the provided transcription using Gemini API."""
    prompt = f"""
        You are an advanced AI assistant trained to extract meaningful insights from transcribed text.
        Your task is to analyze the provided transcript and generate a well-structured Q&A session.

        Instructions:
        - Identify key topics and concepts from the transcription.
        - Generate concise and relevant questions that reflect the main ideas.
        - Provide clear, informative answers in a structured format.

        **Transcript:**  
        ```  
        {transcription}  
        ```  


        Format:
        {{
          "qa_session": [
            {{"question": "<question_text>", "answer": "<answer_text>"}},
            {{"question": "<question_text>", "answer": "<answer_text>"}}
          ]
        }}"""

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)

        # Extract text response
    response_text = response.text if hasattr(response, "text") else "{}"
    
    return json.loads(response_text)
