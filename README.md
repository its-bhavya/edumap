# EduMap — Audio to Mindmap using Agentic AI

**EduMap** is an AI-powered tool that transforms lecture audio into structured, visual mindmaps. It uses:
- **Whisper** for transcription
- **DSPy agents** for semantic structure extraction
- **Graphviz** for mindmap generation
- **Streamlit** for an interactive UI

---

## Demo

---

## Features

1. Upload or record lecture audio  
2. Get accurate transcripts using Whisper  
3. Extract central topics and nested subtopics using DSPy agents  
4. Visualize content as an interactive mindmap
5.  Save all outputs (transcripts, JSON, PNG) automatically

---

## How It Works

1. **Transcribe Audio**: Uses OpenAI Whisper to convert MP3/WAV into text
2. **Extract Concepts**: A DSPy `MindmapExtractor` agent identifies central topics & subtopics
3. **Generate Mindmap**: JSON structure is turned into a mindmap using Graphviz
4. **Render & Display**: Visual shown in real-time via Streamlit

---

## Technologies Used

| Layer            | Tool/Library                 |
|------------------|------------------------------|
| Transcription     | [OpenAI Whisper](https://github.com/openai/whisper) |
| Agent Framework   | [DSPy](https://github.com/stanfordnlp/dspy)         |
| Visualization     | Graphviz (`graphviz.Digraph`)                        |
| Audio Processing  | PyDub                                              |
| UI                | Streamlit                                          |
| API Server        | FastAPI (for extraction endpoint)                   |

---

## Installation

1. **Clone this repo**

```bash
git clone https://github.com/yourname/edumap.git
cd edumap
```

2. **Install Dependencies**

```bash
 pip install -r requirements.txt
```

3. **Install Graphviz**

```bash
# Ubuntu/Debian
sudo apt install graphviz

# macOS
brew install graphviz

# Windows (use choco or installer from [official site]([url](https://graphviz.org/download/)))
choco install graphviz
```

4. **Setup Environment Variable with Gemini API Key**

Create a .env file:
```bash
GOOGLE_API_KEY=your_gemini_key
```
## Running the App

1. **Start the FastAPI backend (DSPy agent):**

```bash
uvicorn app.agents.extractor_agent:app --reload
````

2. **Start the Streamlit frontend:**

```bash
streamlit run main.py
```

3. **Open the app in your browser:**

Visit [http://localhost:8501](http://localhost:8501)

