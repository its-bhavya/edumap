# EduMap — Audio to Mindmap with LLM-Powered Reasoning

**EduMap** is an AI-powered tool that transforms lecture audio into structured, visual mindmaps. 

## Website

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://edumap-ai.streamlit.app/)

## Screenshots

![home-page](https://github.com/user-attachments/assets/a3a5c969-9d78-41ee-b396-31163fe1d41d)
![upload-audio](https://github.com/user-attachments/assets/18045e90-c6ff-43c2-bcf0-6684b2277ba7)
![transcription-ongoing](https://github.com/user-attachments/assets/87000186-f99e-4fdb-9bc2-3bef6db9fee1)
![generated-transcript](https://github.com/user-attachments/assets/7185cae8-49a3-4e2f-8a33-664382234c10)
![generated-mindmap](https://github.com/user-attachments/assets/8e2231de-28f7-420d-8215-b192130c6ee8)


## How It Works
1. **Transcribe Audio**: Uses Assembly AI to convert uploaded or recorded MP3/WAV into text
2. **Extract Concepts**: A DSPy `MindmapExtractor` module identifies central topics & subtopics
3. **Generate Mindmap**: JSON structure is turned into a mindmap using Graphviz
4. **Render & Display**: Visual shown in real-time via Streamlit

## Technologies Used
| Layer            | Tool/Library                 |
|------------------|------------------------------|
| Transcription     | [Assembly AI](https://github.com/AssemblyAI/assemblyai-python-sdk) |
| Agent Framework   | [DSPy](https://github.com/stanfordnlp/dspy)         |
| Visualization     | Graphviz (`graphviz.Digraph`)                        |
| UI                | Streamlit                                          |
| API Server        | FastAPI (for extraction endpoint) + Render (Deployment)                 |

## Installation
1. **Clone this repo**

```bash
git clone https://github.com/its-bhavya/edumap.git
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

# Windows (use choco or installer from official site - https://graphviz.org/download/)
choco install graphviz
```

4. **Setup Environment Variable with Gemini API Key**

Create a .env file:
```bash
GOOGLE_API_KEY=your_gemini_key
ASSEMBLY_API_KEY=your_assembly_api_key
```

5. **Run the App**

a. **Start the FastAPI backend (DSPy agent):**
   ```bash
   uvicorn backend.main:app --reload
   ````
b. **Start the Streamlit frontend:**
   ```bash
   streamlit run frontend/main.py
   ```


