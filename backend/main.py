from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import os, shutil, json, re, sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.utils.transcriber import transcribe, save_to_data
from app.utils.mindmap_generation import generate_mindmap
from app.agents.extractor_agent import MindmapExtractor

load_dotenv()
import dspy
api_key = os.getenv("GOOGLE_API_KEY")
dspy.configure(lm=dspy.LM("gemini/gemini-2.0-flash", api_key=api_key))

app = FastAPI()
extractor = MindmapExtractor()

DATA_DIR = "backend/data"

@app.post("/transcribe")
def transcribe_audio(file: UploadFile = File(...)):
    os.makedirs(os.path.join(DATA_DIR, "audio"), exist_ok=True)
    audio_path = os.path.join(DATA_DIR, "audio", file.filename)
    
    with open(audio_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    text = transcribe(audio_path)
    save_to_data(file.filename, text)
    return {"transcript": text}


class TranscriptRequest(BaseModel):
    transcript: str

@app.post("/extract")
def extract_json(req: TranscriptRequest):
    try:
        result = extractor.forward(transcript=req.transcript)
        def clean_json_field(field: str):
            field = re.sub(r"^```(?:json)?\n?", "", field.strip())
            field = re.sub(r"\n?```$", "", field)
            return json.loads(field)

        subtopics = clean_json_field(result.subtopics)
        data = {"central_topic": result.central_topic, "subtopics": subtopics}

        os.makedirs(f"{DATA_DIR}/json", exist_ok=True)
        json_name = result.central_topic.replace(" ", "-")
        path = f"{DATA_DIR}/json/{json_name}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        # Generate mindmap after JSON is created
        generate_mindmap(path)

        return {"success": True, "central_topic": result.central_topic, "path": path, "data": data}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.get("/mindmap/{topic}")
def get_mindmap(topic: str):
    file_path = os.path.join(DATA_DIR, "mindmaps", f"{topic}.png")
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="image/png")
    return {"error": "Mindmap not found"}
