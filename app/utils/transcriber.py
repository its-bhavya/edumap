from faster_whisper import WhisperModel
import os

model_size = "small" 
model = WhisperModel(model_size, device="cpu")

def transcribe(audio):
    transcription = []
    segments, info = model.transcribe(audio)
    for segment in segments:
        transcription.append(segment.text)
    text = ''.join(transcription)
    return text

def save_to_data(file_name, text):
    os.makedirs("data/transcripts", exist_ok=True)
    save_path = os.path.join("data/transcripts", f"{file_name}.txt")
    with open(save_path, 'w+') as ob:
        ob.write(text)