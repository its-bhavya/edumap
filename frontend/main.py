import streamlit as st
import requests
import time
import tempfile
import os

# 🔧 Set your backend base URL here
API_BASE = "http://localhost:8000"  # or "https://edumap-api.onrender.com"

os.environ["STREAMLIT_DISABLE_WATCHDOG_WARNINGS"] = "1"
st.set_page_config(layout="wide")
st.title("EduMap: Audio to Mindmap")

uploaded_file = st.file_uploader("Upload MP3/WAV Audio of lecture.", type=["mp3", "wav"])
recorded_file = st.audio_input("Record your lecture.")
input_text = st.text_input("Or enter lecture notes as text:")

if "transcript" not in st.session_state:
    st.session_state.transcript = None

# 🎙️ AUDIO MODE
if uploaded_file or recorded_file:
    file = uploaded_file or recorded_file
    st.audio(file)

    if st.button("Transcribe Audio"):
        with st.spinner("Transcribing..."):
            with tempfile.NamedTemporaryFile(suffix=".wav") as tmp:
                tmp.write(file.read())
                tmp.flush()
                tmp.seek(0)
                res = requests.post(f"{API_BASE}/transcribe", files={"file": tmp})
                os.remove(tmp.name)

                if res.status_code == 200:
                    st.session_state.transcript = res.json()["transcript"]
                    st.success("Transcription complete!")
                    st.text_area("Transcript", st.session_state.transcript, height=250)
                else:
                    st.error("Transcription failed.")
                    st.json(res.json())

            

# 📝 TEXT MODE
if input_text:
    st.session_state.transcript = input_text
    st.markdown("### Transcript Preview")
    st.text_area("Transcript", st.session_state.transcript, height=250)

# 🧠 Extract + Visualize Mindmap
if st.session_state.transcript and st.button("Generate Mindmap"):
    with st.spinner("Extracting structure and generating mindmap..."):
        res = requests.post(f"{API_BASE}/extract", json={"transcript": st.session_state.transcript})
        if res.status_code == 200:
            central_topic = res.json()["central_topic"]
            image_url = f"{API_BASE}/mindmap/{central_topic.replace(' ', '-')}"
            st.image(image_url, caption="Generated Mindmap")
        else:
            st.error("Mindmap generation failed.")
            st.json(res.json())
