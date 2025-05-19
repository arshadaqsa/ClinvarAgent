# agents/summarizer.py
import json
from config import MODEL_NAME, client

def generate_summary(variant_data: list[dict]) -> str:
    content = (
        "Summarize the following ClinVar variant metadata in a clinical bioinformatics report. "
        "Focus on genes, pathogenic variants, and their significance.\n\n"
        f"{json.dumps(variant_data, indent=2)}"
    )
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "user", "content": content}
        ]
    )
    return response.choices[0].message.content
