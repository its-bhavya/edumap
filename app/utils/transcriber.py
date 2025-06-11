import whisper
from pydub import AudioSegment
import os
import tempfile

model = whisper.load_model("tiny")  # or "base", "small", etc.

def split_audio(path, chunk_length_ms=30_000):
    audio = AudioSegment.from_file(path)
    chunks = []
    for i in range(0, len(audio), chunk_length_ms):
        chunk = audio[i:i + chunk_length_ms]
        chunk_path = f"temp_chunk_{i // chunk_length_ms}.wav"
        chunk.export(chunk_path, format="wav")
        chunks.append(chunk_path)
    return chunks

def transcribe_chunks(chunk_paths):
    full_transcript = ""
    for chunk_path in chunk_paths:
        result = model.transcribe(chunk_path)
        full_transcript += result["text"].strip() + " "
        os.remove(chunk_path)  # Clean up
    return full_transcript.strip()

def transcribe(audio_path):
    chunks = split_audio(audio_path)
    transcript = transcribe_chunks(chunks)
    return transcript

def save_to_data(file_name, text):
    os.makedirs("data/transcripts", exist_ok=True)
    save_path = os.path.join("data/transcripts", f"{file_name}.txt")
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(text)
