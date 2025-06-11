from dotenv import load_dotenv
import os
import dspy
import json

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

lm = dspy.LM("gemini/gemini-2.0-flash", api_key=api_key)
dspy.configure(lm=lm)

import dspy

class StructureExtractionSignature(dspy.Signature):
    """Extracts a mindmap structure from a transcript of an audio. The mindmap can have multiple layers of hierarchy, condensing information into easy to understand views.
"""

    transcript = dspy.InputField(desc="The full transcript of a lecture or explanation.")

    central_topic = dspy.OutputField(desc="The central concept of the transcript (e.g., 'Photosynthesis').")

    subtopics = dspy.OutputField(
        desc="""
    A raw JSON list where each subtopic has:
    - 'title': string
    - 'description': string
    - optional 'children': a list of similar objects
    """
    )


class MindmapExtractor(dspy.Module):
    def __init__(self):
        super().__init__()
        self.teleprompt = dspy.ChainOfThought(StructureExtractionSignature)

    def forward(self, transcript: str):
        return self.teleprompt(transcript=transcript)

extractor = MindmapExtractor()
with open("data\\transcripts\\ad8e0416-ef1c-4e18-92de-e4a895812abe.txt", "r") as french_revolution:
    transcript = french_revolution.read()

result = extractor.forward(transcript=transcript)
import re

def clean_json_field(field: str):
    field = re.sub(r"^```(?:json)?\n?", "", field.strip())
    field = re.sub(r"\n?```$", "", field)
    return json.loads(field)

subtopics = clean_json_field(result.subtopics)
data = {"central_topic":result.central_topic, "subtopics":subtopics}

with open(f"data\\json\\french_revolution.json", "w+") as ob:
    json.dump(data, ob, indent=2)
