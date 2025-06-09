import streamlit as st
from app.utils.transcriber import transcribe, save_to_data

st.title("Audio Transcription App")

uploaded_file = st.file_uploader("Upload MP3/WAV Audio", type=['mp3', 'wav'])
recorded_file = st.audio_input("Record your audio.")

file = None  # Define safely

if uploaded_file is not None:
    file = uploaded_file
elif recorded_file is not None:
    file = recorded_file

if file:
    st.audio(file, format='audio/wav')  # Optional: playback preview
    file_name = file.file_id
    if st.button("Transcribe"):
        import torch  # Lazy import for compatibility
        transcription = transcribe(file)
        st.subheader("Transcription")
        st.write(transcription)
        save_to_data(file_name, transcription)
