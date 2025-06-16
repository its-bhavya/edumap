import streamlit as st
import requests
import tempfile
import os, io

st.set_page_config(layout="wide")
st.markdown(
    """
    <style>
        .header {
            display: flex;
            align-items: center;
            background-color: #f3f3f3;
            padding: 1rem 2rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
        }
        .header img {
            height: 60px;
            margin-right: 20px;
        }
        .header h1 {
            color: #1a1a1a;
            font-size: 2.2rem;
            font-weight: 700;
            margin: 0;
        }
    </style>

    <div class="header">
        <img src="https://cdn-icons-png.flaticon.com/512/2873/2873617.png" alt="EduMap Logo">
        <h1>EduMap: Lecture to Mindmap</h1>
    </div>
    """,
    unsafe_allow_html=True
)

try:
    API_BASE = st.secrets["API_BASE"] 
except st.errors.StreamlitSecretNotFoundError:
    API_BASE = "http://localhost:8000"


os.environ["STREAMLIT_DISABLE_WATCHDOG_WARNINGS"] = "1"


# --- INPUT SECTION WITH TABS ---
st.markdown("### :material/mic: Input Audio Content")

tab1, tab2, tab3 = st.tabs([" Upload Audio", "Record Audio", "Paste Text"])

if "transcript" not in st.session_state:
    st.session_state.transcript = None

with tab1:
    uploaded_file = st.file_uploader("Upload an MP3/WAV file", type=["mp3", "wav"])
    if uploaded_file:
        if st.button("Transcribe Uploaded Audio"):
            with st.spinner("Transcribing uploaded audio..."):
                files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                res = requests.post(f"{API_BASE}/transcribe", files=files)

            if res.status_code == 200:
                st.session_state.transcript = res.json()["transcript"]
                st.success("Transcription complete.")
            else:
                st.error("Transcription failed.")
                st.json(res.json())

with tab2:
    recorded_file = st.audio_input("Record your lecture.")
    if recorded_file:
        audio_bytes = recorded_file.read()
        st.audio(audio_bytes)

        if st.button("Transcribe Recorded Audio"):
            with st.spinner("Transcribing recorded audio..."):
                try:
                    files = {"file": ("recording.wav", io.BytesIO(audio_bytes), "audio/wav")}
                    res = requests.post(f"{API_BASE}/transcribe", files=files)
                except Exception as e:
                    st.error(f"Transcription request failed: {e}")

                if res.status_code == 200:
                    st.session_state.transcript = res.json()["transcript"]
                    print(st.session_state.transcript)
                else:
                    st.error("Transcription failed.")
                    st.json(res.json())

with tab3:
    input_text = st.text_area("Enter lecture notes here:", height=200)
    if input_text:
        st.session_state.transcript = input_text

# --- TRANSCRIPT PREVIEW ---
if st.session_state.transcript:
    st.markdown("### :material/speech_to_text: Transcript Preview")
    with st.expander("Transcript", expanded=False):
        st.text(st.session_state.transcript)

# --- MINDMAP GENERATION ---
st.markdown("### :material/automation: Generate Mindmap")
if st.session_state.transcript and st.button("View"):
    with st.spinner("Rendering mindmap..."):
        res = requests.post(f"{API_BASE}/extract", json={"transcript": st.session_state.transcript})
        
        if res.status_code == 200:
            st.json(res.json(), expanded=False)
            central_topic = res.json()["central_topic"]

            image_url = f"{API_BASE}/mindmap/{central_topic.replace(' ', '-')}"
            st.image(image_url, caption=f"Mindmap: {central_topic}", use_container_width=True)
        else:
            st.error("Mindmap generation failed.")
            st.json(res.json())
