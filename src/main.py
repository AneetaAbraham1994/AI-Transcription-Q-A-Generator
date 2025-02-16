import os
import requests
import threading
import streamlit as st
import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from utils import save_audio_temp, delete_temp_file, generate_transcription, generate_qa

# Initialize FastAPI app
app = FastAPI()

# Define API request model
class QuestionRequest(BaseModel):
    transcription: str

@app.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...)):
    """
    API to transcribe an uploaded audio file using Whisper.
    """
    tmp_file_path = save_audio_temp(file)
    
    try:
        transcription = generate_transcription(tmp_file_path)
        return {"transcription": transcription}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        delete_temp_file(tmp_file_path)

@app.post("/generate-question/")
async def ask_question(request: QuestionRequest):
    """
    API to generate a Q&A session from transcribed text.
    """
    try:
        qa_data = generate_qa(request.transcription)
        return qa_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run FastAPI in a separate thread
def run_fastapi():
    uvicorn.run(app, host="127.0.0.1", port=8000)

threading.Thread(target=run_fastapi, daemon=True).start()

# ------------------- Streamlit UI -------------------

# API Endpoints
TRANSCRIPTION_API = "http://127.0.0.1:8000/transcribe/"
QA_API = "http://127.0.0.1:8000/generate-question/"

# Streamlit UI
st.set_page_config(page_title="AI Transcription & Q&A", layout="wide")
st.title("🎙️ AI Transcription & Q&A Generator")

# Initialize session state
if "transcription" not in st.session_state:
    st.session_state.transcription = ""
if "qa" not in st.session_state:
    st.session_state.qa = []

# File Upload
st.subheader("📂 Upload an Audio File")
uploaded_file = st.file_uploader("Choose an audio file (MP3/M4A)", type=["mp3", "m4a"])

if uploaded_file:
    st.audio(uploaded_file, format=f"audio/{uploaded_file.name.split('.')[-1]}")
    
    if st.button("📝 Transcribe Audio"):
        with st.spinner("Processing transcription... ⏳"):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
            response = requests.post(TRANSCRIPTION_API, files=files)
        
        if response.status_code == 200:
            st.session_state.transcription = response.json().get("transcription", "")
            st.success("✅ Transcription completed!")
        else:
            st.error(f"❌ Error: {response.json().get('detail', 'Unknown error')}")

# Display Transcription
if st.session_state.transcription:
    st.subheader("📝 Transcribed Text")
    st.text_area("Transcription Output", st.session_state.transcription, height=150)
    
    if st.button("🤖 Generate Q&A"):
        with st.spinner("Generating Q&A... ⏳"):
            response = requests.post(QA_API, json={"transcription": st.session_state.transcription})
        
        if response.status_code == 200:
            st.session_state.qa = response.json().get("qa_session", [])
            st.success("✅ Q&A Generated!")
        else:
            st.error(f"❌ Error: {response.json().get('detail', 'Unknown error')}")

# Display Q&A
if st.session_state.qa:
    st.subheader("💬 AI-Generated Q&A Session")
    
    for qa in st.session_state.qa:
        st.markdown(f"**Q:** {qa['question']}")
        st.markdown(f"**A:** {qa['answer']}")
        st.write("---")
