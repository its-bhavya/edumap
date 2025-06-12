import dspy


class StructureExtractionSignature(dspy.Signature):
    transcript = dspy.InputField(desc="The full transcript of a lecture or explanation.")
    central_topic = dspy.OutputField(desc="The central concept of the transcript.")
    subtopics = dspy.OutputField(
        desc="""A raw JSON list where each subtopic has:
        - 'title': string
        - 'description': string
        - optional 'children': a list of similar objects"""
    )

class MindmapExtractor(dspy.Module):
    def __init__(self):
        super().__init__()
        self.teleprompt = dspy.ChainOfThought(StructureExtractionSignature)

    def forward(self, transcript: str):
        return self.teleprompt(transcript=transcript)
