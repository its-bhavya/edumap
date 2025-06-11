import streamlit as st
import requests
from app.utils.transcriber import transcribe, save_to_data
from app.utils.mindmap_generation import generate_mindmap
import time
import os
import tempfile

os.environ["STREAMLIT_DISABLE_WATCHDOG_WARNINGS"] = "1"

st.title("Edumap")

def extract_mindmap(transcript: str):
    res = requests.post("http://localhost:8000/extract", json={"transcript": transcript})
    if res.status_code == 200:
        data = res.json()
        if data.get("success"):
            return data["path"]
        else:
            st.error("DSPy extraction error: " + data.get("error", "Unknown"))
    else:
        st.error(f"FastAPI server error ({res.status_code})")
    return None

uploaded_file = st.file_uploader("Upload MP3/WAV Audio of lecture.", type=['mp3', 'wav'])
recorded_file = st.audio_input("Record your lecture.")
input_text = st.text_input("Enter your lecture notes.")

file = None  
text_file = None

if uploaded_file:
    file = uploaded_file
elif recorded_file:
    file = recorded_file
elif input_text:
    text_file = input_text

transcription = None
if file:
    st.audio(file, format='audio/wav')
    file_name = file.name
    if st.button("Transcribe"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(uploaded_file.read())
            audio_path = tmp_file.name
        
        import torch
        start = time.time()
        transcription = transcribe(audio_path)
        end = time.time()
        st.write(end-start)
        st.markdown("### Audio Transcript")
        st.write(transcription)
        save_to_data(file_name, transcription)
        
if text_file:
    transcription = text_file
    st.markdown("### Entered text")
    st.write(transcription)

if transcription:
    json_path = extract_mindmap(transcription)
    if json_path:
        chart = generate_mindmap(json_path)
        st.graphviz_chart(chart)
