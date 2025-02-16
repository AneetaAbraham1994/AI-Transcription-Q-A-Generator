# AI-Powered Transcription and Q&A Application

## Overview
The **AI Transcription & Q-A Generator** is an AI-powered application that transcribes audio input and then generates a structured Q&A session based on the transcription. It uses **FastAPI** as the backend service and integrates a **Streamlit** user interface for interactive use. Additionally, the project includes Jupyter notebooks for experimental exploration with the **Whisper transcription API** and the **Gemini Q&A generation API**.

## Features
- **🎧 Audio Transcription:** Upload an audio file (MP3/M4A) to get a transcription.
- **💬 Q&A Generation:** Generate a structured Q&A session from the transcribed text.
- **🖥️ Interactive UI:** A Streamlit interface to upload files and display transcriptions and Q&A sessions.
- **🗃 Experimental Notebooks:** Jupyter notebooks for testing and experimentation with AI models.
- **📝 API Documentation:** Built-in Swagger UI (via FastAPI) for exploring and testing endpoints.

---

## 📌 Setup Instructions

### Prerequisites
- Python **3.12** (or a compatible version)
- **Poetry** for dependency management ([Poetry Installation Guide](https://python-poetry.org/docs/))
- Valid API keys for:
  - **GROQ API** (for Whisper transcription)
  - **Gemini API** (for Q&A generation)

### 🔧 Installation

#### 1️⃣ Install Dependencies Using Poetry:
```bash
poetry init  
poetry config virtualenvs.in-project true  
poetry add streamlit uvicorn fastapi pydantic python-dotenv groq google-generativeai
```
This command creates a virtual environment and installs all required packages as specified in the **pyproject.toml** file.

#### 2️⃣ Configure Environment Variables:
Create a **.env** file in the project root with the following content:
```ini
GROQ_API_KEY=your_groq_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```
Replace the placeholders with your actual API keys.

---

## 🚀 Running the Application

### **Integrated FastAPI & Streamlit App**
To run the application (which starts both the FastAPI backend and the Streamlit UI), execute:
```bash
poetry run streamlit run src/main.py
```
- **Streamlit UI** will launch on **[http://localhost:8501](http://localhost:8501)**.
- **FastAPI backend** will be available at **[http://127.0.0.1:8000](http://127.0.0.1:8000)**.

### **API Documentation**
To view the API documentation (Swagger UI), navigate to:
```bash
http://127.0.0.1:8000/docs
```
This documentation outlines the available endpoints and how to interact with them.

---

## 📚 API Documentation

### **Endpoints**

#### 1️⃣ **POST /transcribe/**
- **Description:** Transcribes an uploaded audio file using the Whisper API.
- **Request:**
  - **Files:** `file` (the audio file, e.g., MP3 or M4A)
- **Response:**
```json
{
  "transcription": "Transcribed text here"
}
```

#### 2️⃣ **POST /ask-question/**
- **Description:** Generates a structured Q&A session from the provided transcription.
- **Request:**
```json
{
  "transcription": "Transcribed text here"
}
```
- **Response:**
```json
{
  "qa_session": [
    {
      "question": "Question text",
      "answer": "Answer text"
    }
  ]
}
```

---

## 🤓 Experimental Notebooks
The project includes two Jupyter notebooks for experimentation, located in the **notebooks/** directory:

- **whisper_experiments.ipynb** → Experimenting with the Whisper transcription API using **GROQ**.
- **gemini_experiments.ipynb** → Experimenting with the Gemini Q&A generation API.

---

## ⚙️ Additional Configurations
- **Environment Variables:** Ensure the `.env` file is correctly set up with your API keys.
- **Deprecation Warnings:** If you encounter warnings (e.g., related to websockets or uvicorn), consider upgrading those packages.

---

## 📝 License
(Include license information here if applicable.)

---

## 📧 Contact
For questions or support, please contact **Aneeta**.

